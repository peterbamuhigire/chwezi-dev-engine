<?php
namespace App\Http\Controllers;

final class ReportController
{
    public function ledger(\PDO $db): array
    {
        $sql = <<<'SQL'
            SELECT c.name, SUM(l.amount) AS balance
            FROM ledger_entries l
            JOIN customers c ON c.id = l.customer_id
            GROUP BY c.name
            SQL;
        return $db->query($sql)->fetchAll();
    }
}
