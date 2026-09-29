<?php
namespace App\Services;

final class StockService
{
    public function __construct(private \PDO $db)
    {
    }

    public function record(int $productId, int $quantity): void
    {
        $this->db->prepare("INSERT INTO stock_movements (product_id, quantity) VALUES (?, ?)")->execute([$productId, $quantity]);
    }
}
