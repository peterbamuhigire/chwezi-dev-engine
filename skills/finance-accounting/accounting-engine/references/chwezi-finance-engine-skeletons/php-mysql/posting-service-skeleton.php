<?php
/**
 * Chwezi posting-service skeleton (PHP / MySQL).
 *
 * Drop-in starting point for the only code path that writes to the ledger.
 * Aligns with the Chwezi Accounting & Finance Doctrine v1.0.0.
 *
 * Forbidden alternatives (any of these is a blocker under the quality gate):
 *   - Direct INSERT / UPDATE / DELETE on journal_headers or journal_lines.
 *   - Single-sided ledger effects.
 *   - Editing posted journals.
 *   - Hardcoded tax rates / thresholds.
 *   - VAT-inclusive postings stored as a single gross figure.
 *
 * Required reads:
 *   - doctrine/accounting-finance-doctrine.md
 *   - doctrine/references/ledger-invariants.md
 *   - doctrine/references/chart-of-accounts.md
 *   - doctrine/references/tax-vat-and-returns.md
 */

namespace Chwezi\Finance\Posting;

use PDO;
use RuntimeException;
use InvalidArgumentException;

final class PostingService
{
    public function __construct(
        private PDO $db,
        private CoaRepository $coa,
        private PeriodStateRepository $periods,
        private TaxCodeRepository $taxCodes,
        private SourceRegisterRepository $sourceRegister,
        private AuditLog $auditLog,
        private IdempotencyStore $idempotency,
        private CurrentUser $actor
    ) {}

    /**
     * Post a balanced journal for an accounting event.
     *
     * @param PostingCommand $cmd
     * @return PostingResult
     * @throws PostingRejected
     */
    public function post(PostingCommand $cmd): PostingResult
    {
        // 1. Idempotency
        if ($prior = $this->idempotency->lookup($cmd->idempotencyKey)) {
            if ($prior->payloadHash !== $cmd->payloadHash()) {
                throw new PostingRejected('idempotency-key-replay-with-different-payload');
            }
            return $prior->result;
        }

        // 2. Period state
        $periodState = $this->periods->stateFor($cmd->entityId, $cmd->bookId, $cmd->date);
        if ($periodState === 'locked' || $periodState === 'archived') {
            throw new PostingRejected("period-state-{$periodState}");
        }
        if ($periodState === 'soft-closed' && !$this->actor->hasRole('Controller')) {
            throw new PostingRejected('soft-closed-requires-controller');
        }

        // 3. Validate lines
        $lines = $this->validateLines($cmd);

        // 4. VAT-inclusive decomposition
        $lines = $this->decomposeVatInclusive($lines, $cmd);

        // 5. Balance check per currency
        $this->assertBalanced($lines);

        // 6. Permissions
        $this->assertDirectPostingAllowed($lines);

        // 7. Evidence
        if (!$this->hasRequiredEvidence($cmd, $lines)) {
            throw new PostingRejected('missing-evidence');
        }

        // 8. Persist inside a single transaction
        $this->db->beginTransaction();
        try {
            $journalId = $this->insertHeader($cmd);
            foreach ($lines as $line) {
                $this->insertLine($journalId, $line);
            }
            $this->updateSubledgers($journalId, $lines);
            $this->db->commit();
        } catch (\Throwable $e) {
            $this->db->rollBack();
            throw new PostingRejected('persist-failed: ' . $e->getMessage(), previous: $e);
        }

        // 9. Audit log
        $this->auditLog->record(
            actor:      $this->actor,
            action:     'post',
            object:     "journal:{$journalId}",
            evidence:   $cmd->evidenceRefs,
            lineage:    null,
            payloadHash: $cmd->payloadHash()
        );

        // 10. Idempotency persist
        $result = new PostingResult($journalId);
        $this->idempotency->store($cmd->idempotencyKey, $cmd->payloadHash(), $result);

        return $result;
    }

    /**
     * Reverse an existing posted journal. The only path to "correct" history.
     * Edit and delete are not supported.
     */
    public function reverse(int $originalJournalId, ReversalReason $reason, bool $partial = false): PostingResult
    {
        $original = $this->loadHeaderOrFail($originalJournalId);
        if ($original->state === 'reversed') {
            throw new PostingRejected('already-reversed');
        }

        // Apply maker-checker policy
        $this->assertApprovedForReversal($original, $reason);

        $reversalCmd = ReversalCommandFactory::fromOriginal($original, $reason, $partial, $this->actor);
        $result = $this->post($reversalCmd);

        // Link reversal lineage
        $this->markReversed($originalJournalId, $result->journalId, $reason, $this->actor);

        return $result;
    }

    // -----------------------------------------------------------------
    // Helpers — implementations elided in this skeleton; see doctrine.
    // -----------------------------------------------------------------

    private function validateLines(PostingCommand $cmd): array
    {
        // Validate every line against CoA, tax-code, dimensions matrix.
        return $cmd->lines;
    }

    private function decomposeVatInclusive(array $lines, PostingCommand $cmd): array
    {
        // For each VAT-inclusive line, replace it with net + tax lines.
        // Rate is read from $this->taxCodes (which consults the source register).
        return $lines;
    }

    private function assertBalanced(array $lines): void
    {
        $byCcy = [];
        foreach ($lines as $l) {
            $byCcy[$l->currency] = ($byCcy[$l->currency] ?? 0) + ($l->debit - $l->credit);
        }
        foreach ($byCcy as $ccy => $delta) {
            if (abs($delta) > 0) {
                throw new PostingRejected("unbalanced-{$ccy}-by-{$delta}");
            }
        }
    }

    private function assertDirectPostingAllowed(array $lines): void
    {
        foreach ($lines as $l) {
            $rule = $this->coa->byCode($l->accountCode)->directPosting;
            if ($rule === 'system-only') {
                throw new PostingRejected("system-only-account-{$l->accountCode}");
            }
            if ($rule === 'restricted-to-controller' && !$this->actor->hasRole('Controller')) {
                throw new PostingRejected("controller-restricted-account-{$l->accountCode}");
            }
        }
    }

    private function hasRequiredEvidence(PostingCommand $cmd, array $lines): bool
    {
        foreach ($lines as $l) {
            $required = $this->coa->byCode($l->accountCode)->evidenceRequired;
            if ($required === 'always' && count($cmd->evidenceRefs) === 0) {
                return false;
            }
            if ($required === 'over-threshold') {
                $threshold = $this->coa->byCode($l->accountCode)->evidenceThreshold;
                if (abs($l->debit - $l->credit) >= $threshold && count($cmd->evidenceRefs) === 0) {
                    return false;
                }
            }
        }
        return true;
    }

    private function insertHeader(PostingCommand $cmd): int
    {
        $stmt = $this->db->prepare(
            'INSERT INTO journal_headers
              (entity_id, book_id, date, period, source_document, idempotency_key,
               actor_user_id, actor_role, posting_service_version, status, created_at)
             VALUES
              (:entity, :book, :date, :period, :doc, :idem, :user, :role, :ver, :status, NOW())'
        );
        $stmt->execute([
            ':entity' => $cmd->entityId,
            ':book'   => $cmd->bookId,
            ':date'   => $cmd->date->format('Y-m-d'),
            ':period' => $cmd->date->format('Y-m'),
            ':doc'    => $cmd->sourceDocumentRef,
            ':idem'   => $cmd->idempotencyKey,
            ':user'   => $this->actor->id,
            ':role'   => $this->actor->roleContext,
            ':ver'    => self::class . '@1.0.0',
            ':status' => 'posted'
        ]);
        return (int) $this->db->lastInsertId();
    }

    private function insertLine(int $journalId, JournalLine $line): void
    {
        $stmt = $this->db->prepare(
            'INSERT INTO journal_lines
              (journal_id, account_code, debit, credit, currency,
               tax_code, dimensions_json, description, source_line_ref)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        );
        $stmt->execute([
            $journalId, $line->accountCode, $line->debit, $line->credit, $line->currency,
            $line->taxCode, json_encode($line->dimensions), $line->description, $line->sourceLineRef
        ]);
    }

    private function updateSubledgers(int $journalId, array $lines): void
    {
        // For each line whose account is a control account, write to the
        // subledger (AR, AP, Inventory, FA, Tax, Payroll, …) here.
    }

    private function loadHeaderOrFail(int $id): JournalHeader
    {
        // …
        throw new RuntimeException('not implemented in skeleton');
    }

    private function assertApprovedForReversal(JournalHeader $h, ReversalReason $r): void
    {
        // Maker-checker check; threshold check.
    }

    private function markReversed(int $original, int $reversal, ReversalReason $r, CurrentUser $a): void
    {
        // Persist linkage.
    }
}
