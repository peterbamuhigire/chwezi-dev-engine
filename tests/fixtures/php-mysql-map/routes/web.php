<?php
// Synthetic fixture: five routes, one per controller.
use App\Http\Controllers\InvoiceController;
use App\Http\Controllers\CustomerController;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\PaymentController;
use App\Http\Controllers\ReportController;

Route::get('/invoices', [InvoiceController::class, 'index']);
Route::post('/customers', [CustomerController::class, 'store']);
Route::put('/products/{id}', [ProductController::class, 'update']);
Route::post('/payments', [PaymentController::class, 'store']);
Route::get('/reports/ledger', 'ReportController@ledger');
