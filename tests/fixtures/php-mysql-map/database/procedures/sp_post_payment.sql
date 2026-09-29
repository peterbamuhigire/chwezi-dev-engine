-- Synthetic fixture procedure.
DELIMITER $$
CREATE PROCEDURE sp_post_payment(IN p_invoice_id BIGINT, IN p_amount DECIMAL(15,2))
BEGIN
  INSERT INTO payments (invoice_id, amount) VALUES (p_invoice_id, p_amount);
  INSERT INTO ledger_entries (invoice_id, amount) VALUES (p_invoice_id, p_amount);
END$$
DELIMITER ;
