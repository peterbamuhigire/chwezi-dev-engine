<?php
namespace App\Http\Controllers;

use App\Models\Product;
use App\Services\StockService;

final class ProductController
{
    public function update(int $id, array $input, StockService $stock): void
    {
        $product = Product::find($id);
        $stock->record($id, (int) ($input['quantity'] ?? 0));
    }
}
