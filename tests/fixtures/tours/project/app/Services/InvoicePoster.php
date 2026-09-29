<?php
// Synthetic fixture for tests/test_validate_tour.py. Not application code.
declare(strict_types=1);

namespace App\Services;

final class InvoicePoster
{
    public function __construct(private \PDO $db)
    {
    }

    public function post(int $tenantId, int $invoiceId): void
    {
        $this->db->beginTransaction();
        $stmt = $this->db->prepare('SELECT total FROM invoices WHERE tenant_id = ? AND id = ?');
        $stmt->execute([$tenantId, $invoiceId]);
        $total = (int) $stmt->fetchColumn();
        $insert = $this->db->prepare('INSERT INTO journal_lines (tenant_id, invoice_id, amount) VALUES (?, ?, ?)');
        $insert->execute([$tenantId, $invoiceId, $total]);
        $this->db->commit();
    }
}
