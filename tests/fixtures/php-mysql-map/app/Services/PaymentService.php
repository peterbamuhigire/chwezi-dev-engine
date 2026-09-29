<?php
namespace App\Services;

final class PaymentService
{
    public function __construct(private $gateway)
    {
    }

    public function post(int $invoiceId, string $amount): void
    {
        // table access happens inside the stored procedure
        $this->gateway->call('sp_post_payment', [$invoiceId, $amount]);
    }
}
