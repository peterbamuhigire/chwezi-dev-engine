<?php
declare(strict_types=1);
require __DIR__ . '/invoice-list.php';
$pdo = new PDO('sqlite::memory:', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec('PRAGMA foreign_keys=ON');
$pdo->exec('CREATE TABLE customers (id INTEGER PRIMARY KEY, tenant_id INTEGER NOT NULL, name TEXT NOT NULL, UNIQUE (tenant_id,id))');
$pdo->exec('CREATE TABLE invoices (id INTEGER PRIMARY KEY, tenant_id INTEGER NOT NULL, customer_id INTEGER NOT NULL, number TEXT NOT NULL, currency TEXT NOT NULL, amount_minor INTEGER NOT NULL, FOREIGN KEY(tenant_id,customer_id) REFERENCES customers(tenant_id,id))');
$pdo->exec('CREATE INDEX invoices_tenant_id ON invoices(tenant_id,id)');
$pdo->exec('CREATE TABLE journal_lines (id INTEGER PRIMARY KEY, amount_minor INTEGER NOT NULL)');
$pdo->exec("INSERT INTO customers VALUES (1,1,'<script>alert(1)</script>'), (2,2,'Private tenant two')");
$pdo->exec("INSERT INTO invoices VALUES (1,1,1,'INV-001','UGX',12000),(2,2,2,'INV-001','UGX',99000),(3,1,1,'INV-002','UGX',23000)");
$repository = new PdoInvoiceRepository($pdo);
$controller = new InvoiceController(new ListInvoices($repository));
$context = new InvoiceContext(1, true);
$tests = 0;
function check(bool $value, string $name): void {
    global $tests;
    if (!$value) { throw new RuntimeException('FAIL ' . $name); }
    $tests++;
    echo 'PASS ' . $name . PHP_EOL;
}
$result = $controller->get($context, ['tenant_id' => 2]);
check($result['status'] === 200 && count($result['body']['data']) === 2, 'tenant scope ignores forged request tenant');
check(array_column($result['body']['data'], 'id') === ['1','3'], 'tenant two rows excluded');
check($repository->queryCount === 1, 'joined list uses one query');
check($result['headers']['Cache-Control'] === 'private, no-store', 'private response');
check($controller->get($context, ['q' => "' OR 1=1 --"])['body']['data'] === [], 'injection remains literal');
check($controller->get(null, [])['status'] === 401, 'missing authentication rejected');
$before = $repository->queryCount;
check($controller->get(new InvoiceContext(1, false), [])['status'] === 403, 'permission denied');
check($repository->queryCount === $before, 'denial performs no database query');
check($controller->get($context, ['limit' => 101])['status'] === 400, 'oversized page rejected');
check($controller->get($context, ['q' => ['bad']])['status'] === 400, 'array query rejected');
check(count($controller->get($context, ['limit' => 1])['body']['data']) === 1, 'page bound honoured');
$html = renderInvoices($result['body']['data']);
check(!str_contains($html, '<script>') && str_contains($html, '&lt;script&gt;'), 'HTML content escaped');
check(str_contains(renderInvoices([]), 'No invoices found.'), 'empty state explicit');
check((int) $pdo->query('SELECT COUNT(*) FROM journal_lines')->fetchColumn() === 0, 'listing does not post journals');
try { $pdo->exec("INSERT INTO invoices VALUES(4,1,2,'BAD','UGX',1)"); $rejected = false; }
catch (PDOException) { $rejected = true; }
check($rejected, 'cross-tenant customer reference rejected by constraint');
echo "$tests checks passed; PDO SQLite synthetic fixture, not MySQL deployment proof" . PHP_EOL;
