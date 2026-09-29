<?php
// Synthetic fixture migration.
Schema::create('audit_log', function ($table) {
    $table->id();
});
