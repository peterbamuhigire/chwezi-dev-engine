<?php
namespace App\Http\Controllers;

use App\Services\CustomerService;

final class CustomerController
{
    public function __construct(private CustomerService $customers)
    {
    }

    public function store(array $input): int
    {
        return $this->customers->create($input);
    }
}
