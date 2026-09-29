<?php
namespace App\Http\Controllers;

final class InvoiceController
{
    public function index(\PDO $db): array
    {
        // literal SQL in the controller
        $sql = 'SELECT i.id, i.total, it.sku FROM invoices i JOIN invoice_items it ON it.invoice_id = i.id WHERE i.tenant_id = ?';
        return $db->prepare($sql)->fetchAll();
    }
}
