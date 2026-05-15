-- Chwezi Finance Engine schema skeleton — aligned to doctrine v1.0.0.
-- MySQL 8 / MariaDB 10.6+. Adjust to your engine; never weaken the invariants.

-- =============================================================================
-- Chart of Accounts
-- =============================================================================
CREATE TABLE coa_accounts (
  code            VARCHAR(20)  NOT NULL PRIMARY KEY,
  name            VARCHAR(200) NOT NULL,
  class           ENUM('asset','liability','equity','income','expense') NOT NULL,
  statement_group VARCHAR(80)  NOT NULL,
  normal_side     ENUM('debit','credit') NOT NULL,
  direction_rule  ENUM('enforced','flexible') NOT NULL DEFAULT 'flexible',
  is_contra       TINYINT(1)   NOT NULL DEFAULT 0,
  is_control      TINYINT(1)   NOT NULL DEFAULT 0,
  subledger_key   VARCHAR(40)  NULL,
  tax_flag        ENUM('none','output-vat','input-vat','wht-payable','paye-payable','nssf-payable','tax-receivable')
                   NOT NULL DEFAULT 'none',
  currency_rule   ENUM('entity-currency-only','multi-currency-allowed','foreign-currency-only') NOT NULL,
  dimensions_required JSON NOT NULL,    -- ["branch","cost-centre",…]
  dimensions_permitted JSON NOT NULL,
  direct_posting  ENUM('permitted','restricted-to-controller','system-only') NOT NULL,
  reconciliation_required ENUM('daily','monthly','quarterly','annually','event-driven','none')
                   NOT NULL DEFAULT 'none',
  evidence_required ENUM('always','over-threshold','none') NOT NULL DEFAULT 'none',
  evidence_threshold DECIMAL(20,4) NULL,
  owner_role      VARCHAR(40)  NOT NULL,
  active_from     DATE         NOT NULL,
  active_to       DATE         NULL,
  INDEX (statement_group), INDEX (tax_flag)
);

-- =============================================================================
-- Period state
-- =============================================================================
CREATE TABLE period_state (
  entity_id   BIGINT NOT NULL,
  book_id     BIGINT NOT NULL,
  period      CHAR(7) NOT NULL,        -- YYYY-MM
  state       ENUM('open','soft-closed','locked','reopened','archived') NOT NULL DEFAULT 'open',
  changed_by  BIGINT NOT NULL,
  changed_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  reason      TEXT NULL,
  PRIMARY KEY (entity_id, book_id, period)
);

-- =============================================================================
-- Journals — append-only; no UPDATE / DELETE through application paths.
-- =============================================================================
CREATE TABLE journal_headers (
  id              BIGINT AUTO_INCREMENT PRIMARY KEY,
  entity_id       BIGINT NOT NULL,
  book_id         BIGINT NOT NULL,
  date            DATE NOT NULL,
  period          CHAR(7) NOT NULL,
  source_document VARCHAR(200) NOT NULL,
  idempotency_key VARCHAR(120) NOT NULL,
  actor_user_id   BIGINT NOT NULL,
  actor_role      VARCHAR(40) NOT NULL,
  posting_service_version VARCHAR(80) NOT NULL,
  status          ENUM('posted','reversed','correction') NOT NULL,
  reverses_journal_id BIGINT NULL,
  reversal_reason VARCHAR(80) NULL,
  reversal_type   ENUM('full','partial') NULL,
  created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_idem (idempotency_key),
  INDEX (entity_id, book_id, period),
  INDEX (date)
);

CREATE TABLE journal_lines (
  id              BIGINT AUTO_INCREMENT PRIMARY KEY,
  journal_id      BIGINT NOT NULL,
  account_code    VARCHAR(20) NOT NULL,
  debit           DECIMAL(24,4) NOT NULL DEFAULT 0,
  credit          DECIMAL(24,4) NOT NULL DEFAULT 0,
  currency        CHAR(3) NOT NULL,
  tax_code        VARCHAR(40) NULL,
  dimensions_json JSON NOT NULL,
  description     VARCHAR(400) NULL,
  source_line_ref VARCHAR(120) NULL,
  CONSTRAINT fk_jl_h FOREIGN KEY (journal_id) REFERENCES journal_headers(id),
  CONSTRAINT chk_dr_xor_cr CHECK ((debit > 0) <> (credit > 0) OR (debit = 0 AND credit = 0)),
  INDEX (account_code, journal_id),
  INDEX (tax_code)
);

-- Trigger guard: refuse UPDATE / DELETE on journal_lines / headers
DELIMITER //
CREATE TRIGGER trg_jh_no_update BEFORE UPDATE ON journal_headers FOR EACH ROW
BEGIN
  IF OLD.status <> NEW.status AND OLD.status = 'posted' AND NEW.status = 'reversed' THEN
    -- allow flip to reversed via posting service
    SET NEW.status = NEW.status;
  ELSEIF OLD.status = 'posted' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'journal_headers UPDATE forbidden on posted records';
  END IF;
END//
CREATE TRIGGER trg_jh_no_delete BEFORE DELETE ON journal_headers FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'journal_headers DELETE forbidden';
END//
CREATE TRIGGER trg_jl_no_update BEFORE UPDATE ON journal_lines FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'journal_lines UPDATE forbidden';
END//
CREATE TRIGGER trg_jl_no_delete BEFORE DELETE ON journal_lines FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'journal_lines DELETE forbidden';
END//
DELIMITER ;

-- =============================================================================
-- Audit log — append-only
-- =============================================================================
CREATE TABLE audit_log (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  ts          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actor_user  BIGINT NOT NULL,
  actor_role  VARCHAR(40) NOT NULL,
  service_id  VARCHAR(80) NOT NULL,
  action      VARCHAR(80) NOT NULL,
  object      VARCHAR(120) NOT NULL,
  before_json JSON NULL,
  after_json  JSON NULL,
  evidence_refs JSON NULL,
  payload_hash CHAR(64) NULL,
  INDEX (ts), INDEX (actor_user), INDEX (object)
);

-- =============================================================================
-- Idempotency store
-- =============================================================================
CREATE TABLE idempotency_keys (
  idempotency_key VARCHAR(120) PRIMARY KEY,
  payload_hash    CHAR(64) NOT NULL,
  result_json     JSON NOT NULL,
  stored_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- Source register (live-rate verification)
-- =============================================================================
CREATE TABLE source_register (
  id             BIGINT AUTO_INCREMENT PRIMARY KEY,
  jurisdiction   CHAR(2) NOT NULL,
  topic          VARCHAR(80) NOT NULL,
  value_or_rule  TEXT NOT NULL,
  source_url     TEXT NOT NULL,
  source_tier    TINYINT NOT NULL,
  date_accessed  DATE NOT NULL,
  verifier       VARCHAR(120) NOT NULL,
  output_affected JSON NOT NULL,
  expiry_or_recheck DATE NOT NULL,
  state          ENUM('draft','pass-with-caveats','verified-current','blocked') NOT NULL,
  evidence_archive TEXT NULL,
  notes          TEXT NULL,
  effective_from DATE NOT NULL,
  effective_to   DATE NULL,
  INDEX (jurisdiction, topic, state, effective_from)
);

-- =============================================================================
-- Tax codes
-- =============================================================================
CREATE TABLE tax_codes (
  code           VARCHAR(40) PRIMARY KEY,
  jurisdiction   CHAR(2) NOT NULL,
  kind           ENUM('vat','wht','paye','nssf','customs','excise','other') NOT NULL,
  rate           DECIMAL(8,4) NULL,
  rate_basis     ENUM('percent','fixed','table') NOT NULL DEFAULT 'percent',
  effective_from DATE NOT NULL,
  effective_to   DATE NULL,
  source_register_id BIGINT NULL,
  FOREIGN KEY (source_register_id) REFERENCES source_register(id),
  INDEX (jurisdiction, kind, effective_from)
);
