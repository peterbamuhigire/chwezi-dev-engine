CREATE TABLE customers (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    tenant_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY customers_tenant_id_id_uq (tenant_id, id)
) ENGINE=InnoDB;

CREATE TABLE invoices (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    tenant_id BIGINT UNSIGNED NOT NULL,
    customer_id BIGINT UNSIGNED NOT NULL,
    number VARCHAR(64) NOT NULL,
    currency CHAR(3) NOT NULL,
    amount_minor BIGINT NOT NULL,
    PRIMARY KEY (id),
    KEY invoices_tenant_id_id_idx (tenant_id, id),
    CONSTRAINT invoices_customer_same_tenant_fk
        FOREIGN KEY (tenant_id, customer_id)
        REFERENCES customers (tenant_id, id)
) ENGINE=InnoDB;
