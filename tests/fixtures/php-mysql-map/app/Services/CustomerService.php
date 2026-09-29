<?php
namespace App\Services;

final class CustomerService
{
    public function __construct(private \PDO $db)
    {
    }

    public function create(array $input): int
    {
        $this->db->prepare('INSERT INTO customers (tenant_id, name) VALUES (?, ?)')->execute([$input['tenant_id'], $input['name']]);
        DB::table('audit_log')->insert(['event' => 'customer.created']);
        return (int) $this->db->lastInsertId();
    }
}
