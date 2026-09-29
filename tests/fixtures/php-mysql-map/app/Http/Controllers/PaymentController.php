<?php
namespace App\Http\Controllers;

use App\Services\PaymentService;

final class PaymentController
{
    public function store(array $input, PaymentService $payments): void
    {
        $payments->post((int) $input['invoice_id'], (string) $input['amount']);
    }
}
