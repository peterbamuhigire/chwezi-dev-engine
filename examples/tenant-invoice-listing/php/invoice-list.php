<?php
declare(strict_types=1);

// Synthetic executable teaching fixture. Authentication is supplied by its caller.
final readonly class InvoiceContext
{
    public function __construct(public int $tenantId, public bool $canReadInvoices)
    {
        if ($tenantId < 1) { throw new InvalidArgumentException('Verified tenant required'); }
    }
}

interface InvoiceRepository
{
    public function list(InvoiceContext $context, string $search, int $limit): array;
}

final class PdoInvoiceRepository implements InvoiceRepository
{
    public int $queryCount = 0;
    public function __construct(private readonly PDO $pdo) {}
    public function list(InvoiceContext $context, string $search, int $limit): array
    {
        $statement = $this->pdo->prepare(
            'SELECT i.id, i.number, i.currency, i.amount_minor, c.name AS customer '
            . 'FROM invoices i JOIN customers c ON c.id=i.customer_id AND c.tenant_id=i.tenant_id '
            . 'WHERE i.tenant_id=:tenant AND i.number LIKE :search '
            . 'ORDER BY i.id LIMIT :limit'
        );
        $statement->bindValue(':tenant', $context->tenantId, PDO::PARAM_INT);
        $statement->bindValue(':search', '%' . $search . '%', PDO::PARAM_STR);
        $statement->bindValue(':limit', $limit, PDO::PARAM_INT);
        $this->queryCount++;
        $statement->execute();
        return array_map(
            // Keep SQL BIGINT values as decimal text at the JSON boundary.
            static fn (array $row): array => [
                ...$row,
                'id' => (string) $row['id'],
                'amount_minor' => (string) $row['amount_minor'],
            ],
            $statement->fetchAll(PDO::FETCH_ASSOC),
        );
    }
}

final class ListInvoices
{
    public function __construct(private readonly InvoiceRepository $repository) {}
    public function run(InvoiceContext $context, string $search, int $limit): array
    {
        if (!$context->canReadInvoices) { throw new DomainException('Invoice permission required'); }
        if ($limit < 1 || $limit > 100 || strlen($search) > 120) {
            throw new InvalidArgumentException('Invalid listing bounds');
        }
        return $this->repository->list($context, $search, $limit);
    }
}

final class InvoiceController
{
    public function __construct(private readonly ListInvoices $service) {}
    public function get(?InvoiceContext $authenticatedContext, array $query): array
    {
        // Never derive the context from tenant_id in request parameters.
        if ($authenticatedContext === null) { return ['status' => 401, 'body' => ['error' => 'Unauthenticated']]; }
        try {
            $limit = filter_var($query['limit'] ?? 20, FILTER_VALIDATE_INT);
            if ($limit === false || !is_string($query['q'] ?? '')) { throw new InvalidArgumentException('Invalid input'); }
            $data = $this->service->run($authenticatedContext, $query['q'] ?? '', $limit);
            return ['status' => 200, 'headers' => ['Cache-Control' => 'private, no-store'], 'body' => ['data' => $data]];
        } catch (DomainException) {
            return ['status' => 403, 'body' => ['error' => 'Forbidden']];
        } catch (InvalidArgumentException) {
            return ['status' => 400, 'body' => ['error' => 'Invalid listing request']];
        }
    }
}

function renderInvoices(array $rows): string
{
    if ($rows === []) { return '<p role="status">No invoices found.</p>'; }
    $html = '<table><caption>Invoices</caption><thead><tr><th scope="col">Number</th><th scope="col">Customer</th><th scope="col">Currency</th><th scope="col">Amount in minor units</th></tr></thead><tbody>';
    foreach ($rows as $row) {
        $html .= '<tr>';
        foreach (['number', 'customer', 'currency', 'amount_minor'] as $field) {
            $html .= '<td>' . htmlspecialchars((string) $row[$field], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</td>';
        }
        $html .= '</tr>';
    }
    return $html . '</tbody></table>';
}
