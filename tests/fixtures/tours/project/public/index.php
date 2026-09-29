<?php
// Synthetic fixture for tests/test_validate_tour.py. Not application code.
declare(strict_types=1);

require __DIR__ . '/../app/bootstrap.php';

$tenant = resolve_tenant($_SERVER['HTTP_HOST'] ?? '');
if ($tenant === null) {
    http_response_code(404);
    exit;
}

route($tenant, $_SERVER['REQUEST_URI'] ?? '/');
