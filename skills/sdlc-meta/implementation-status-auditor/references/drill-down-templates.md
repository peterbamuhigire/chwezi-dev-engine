# Drill-Down Templates for Iterative Auditing

After the initial audit, users can request deep dives. Use these templates.

## Module Deep Dive Template

**File:** `06-module-details/{module-name}-status.md`

```markdown
# Module Deep Dive: {Module Name}

**Overall Status:** Complete | Partial ({X}%) | Missing
**Priority:** Critical | High | Medium | Low
**Estimated Effort to Complete:** S | M | L | XL

## Architecture Overview

{Brief description of how this module fits into the system}

### Components

| Component | Type | Status | File Path | Evidence |
|-----------|------|--------|-----------|----------|
| {name} | Model | ✅ Complete | `app/Models/X.php` | EXTRACTED: read `app/Models/X.php:12-40` |
| {name} | Controller | ⚠️ Partial | `app/Http/Controllers/X.php` | INFERRED: LSP callers, index built {timestamp} at {full commit SHA}; verify in source before editing |
| {name} | Migration | ✅ Complete | `database/migrations/X.php` | EXTRACTED: `Schema::create('x', ...)` at line 14 |
| {name} | Route | ❌ Missing | — | EXTRACTED: `git grep -n "XController" routes/` returned nothing |
| {name} | UI Screen | ❌ Missing | — | AMBIGUOUS: view name built from a variable in `XController::show`; flagged for review |
| {name} | Test | ❌ Missing | — | EXTRACTED: no file under `tests/` names `X` |

**Evidence tags.** Every status row carries one tag:

| Tag | Meaning | Worked row |
|---|---|---|
| EXTRACTED | Read directly from source at the audited commit | `InvoiceController`, ✅ Complete. EXTRACTED: `routes/web.php:41` maps `POST /invoices` to `InvoiceController@store` |
| INFERRED | Resolved by a tool or by reasoning; verify in source before acting | `CreditNoteService`, ⚠️ Partial. INFERRED: the index shows 2 callers; index built 2026-09-29T08:14Z at full commit `3f9c2a7e5b1d4c8f9a0b6e2d7c1f4a8b9e0d3c5a` |
| AMBIGUOUS | Cannot be resolved statically; never counted as absent | `ReportExporter`, status unknown. AMBIGUOUS: the class name is built from `$type` at runtime; needs a runtime check |

Structural-index evidence (LSP, ctags, a project map or a graph file) is accepted only when the row
records the index build timestamp and the full commit SHA it was built from. An index result without
both is treated as AMBIGUOUS. For PHP, "no callers" from an index also needs a grep on the method
name (see `ai-assisted-development/references/graph-first-codebase-comprehension.md`). Tag
vocabulary adapted from Graphify-Labs/graphify (Apache-2.0, https://github.com/Graphify-Labs/graphify,
commit `d6eaa8aae8df155874ebb1044302c055c286342a`).

## Database Tables

| Table | Columns | Indexes | FKs | Status |
|-------|---------|---------|-----|--------|
| {table} | {count} | {count} | {count} | ✅ / ⚠️ / ❌ |

### Schema Issues
- {issue description}

## API Endpoints

| Method | Path | Auth | Status | Notes |
|--------|------|------|--------|-------|
| GET | /api/{resource} | JWT | ✅ | Paginated |
| POST | /api/{resource} | JWT | ⚠️ | No validation |
| PUT | /api/{resource}/{id} | JWT | ❌ | Not implemented |
| DELETE | /api/{resource}/{id} | JWT | ❌ | Not implemented |

## Business Logic Status

| Rule | Documented In | Implemented | Tested |
|------|--------------|-------------|--------|
| {rule} | {doc ref} | ✅ / ❌ | ✅ / ❌ |

## What Remains

| # | Task | Complexity | Skill | Depends On |
|---|------|-----------|-------|------------|
| 1 | {task} | S/M/L/XL | `{skill}` | {dep or None} |

## Recommended Implementation Order

1. {step} — why this goes first
2. {step} — depends on step 1
3. {step} — final integration
```

## API Payload Deep Dive Template

**Use when:** User asks "Show me the API payloads for {feature}"

```markdown
# API Payload Analysis: {Feature Name}

## Endpoint: {METHOD} {path}

### Request

**Headers:**
| Header | Value | Required |
|--------|-------|----------|
| Authorization | Bearer {token} | Yes |
| Content-Type | application/json | Yes |
| X-Tenant-ID | {tenant_id} | Yes (multi-tenant) |

**Request Body (based on schema):**
```json
{
  "field_name": "type — description (from DB column)",
  "field_name": "type — description"
}
```

**Validation Rules (from code/docs):**
| Field | Type | Required | Rules |
|-------|------|----------|-------|
| {field} | string | Yes | max:255 |

### Response

**Success (200):**
```json
{
  "status": "success",
  "data": {
    "id": "int",
    "field": "type — from {table}.{column}"
  }
}
```

**Error (4xx):**
```json
{
  "status": "error",
  "message": "string",
  "errors": {}
}
```

### Current vs Expected

| Field | In Schema | In API Response | Match |
|-------|----------|-----------------|-------|
| {field} | ✅ | ✅ | ✅ |
| {field} | ✅ | ❌ | ❌ Gap |
| {field} | ❌ | ✅ | ⚠️ Undocumented |
```

## Test Coverage Deep Dive Template

**Use when:** User asks "What tests are missing for {module}"

```markdown
# Test Coverage Analysis: {Module Name}

## Current Test Inventory

| Test File | Type | Tests | Pass | Fail | Skip |
|-----------|------|-------|------|------|------|
| {file} | Unit | {n} | {n} | {n} | {n} |
| {file} | Integration | {n} | {n} | {n} | {n} |

## Missing Tests

### Unit Tests Needed
| # | Test Case | Component | Priority | Skill |
|---|-----------|-----------|----------|-------|
| 1 | {description} | {class/method} | High | `sdlc-testing` |

### Integration Tests Needed
| # | Test Case | Endpoints | Priority |
|---|-----------|-----------|----------|
| 1 | {description} | {endpoints} | High |

### E2E Tests Needed
| # | User Flow | Screens | Priority |
|---|-----------|---------|----------|
| 1 | {description} | {screens} | Medium |

## Test Pyramid Status

```
Target:    Current:
  E2E 10%     E2E {X}%
 Int  20%    Int  {X}%
Unit  70%   Unit  {X}%
```

## Recommended Testing Order
1. {test} — covers critical path
2. {test} — covers data integrity
3. {test} — covers edge cases
```

## Schema Entity Map Template

**File:** `07-appendices/schema-entity-map.md`

```markdown
# Schema-to-Feature Entity Map

## Legend
- ✅ Table exists and supports feature
- ⚠️ Table exists but incomplete (missing columns/indexes)
- ❌ Table missing entirely
- 🔗 Junction/pivot table

## Entity Mapping

| Documented Feature | Required Tables | Status | Notes |
|-------------------|----------------|--------|-------|
| User Management | users, roles, permissions | ✅ | Complete |
| Inventory | products, stock_movements | ⚠️ | Missing indexes |
| Reporting | report_templates | ❌ | Phantom feature |

## Orphan Tables (in schema, no matching feature)

| Table | Columns | Rows | Possible Purpose |
|-------|---------|------|-----------------|
| {table} | {n} | {n} | {guess based on structure} |
```

## Completion Phase Expansion Template

**Use when:** User asks "Generate the completion plan for Phase {N}"

```markdown
# Completion Plan — Phase {N}: {Phase Name}

## Phase Overview
**Goal:** {what this phase accomplishes}
**Prerequisites:** Phase {N-1} complete
**Estimated Total Effort:** {sum of task complexities}

## Detailed Task Breakdown

### Task {N}.1: {Task Name}
**Module:** {module}
**Complexity:** M
**Skill:** `{skill-name}`
**Depends on:** None

**Steps:**
1. {specific step with file path}
2. {specific step}
3. {specific step}

**Acceptance Criteria:**
- [ ] {criterion}
- [ ] {criterion}
- [ ] Tests pass

**Files to Create/Modify:**
| Action | File Path | Description |
|--------|-----------|-------------|
| Create | `path/to/file` | {what} |
| Modify | `path/to/file` | {what changes} |

---
(Repeat for each task in the phase)
```

## Re-Audit Comparison Template

**Use when:** Running a follow-up audit to compare progress.

```markdown
# Re-Audit Comparison: {date1} vs {date2}

## Progress Summary

| Metric | Previous | Current | Delta |
|--------|----------|---------|-------|
| Health Score | X/10 | X/10 | +X |
| Complete Features | X | X | +X |
| Partial Features | X | X | -X |
| Phantom Features | X | X | -X |
| Critical Risks | X | X | -X |

## Features Completed Since Last Audit
| Feature | Module | Completed Date |
|---------|--------|---------------|
| {feature} | {module} | {date} |

## New Issues Found
| Issue | Severity | Module |
|-------|----------|--------|
| {issue} | {severity} | {module} |

## Updated Blueprint
(Reference the new `05-completion-blueprint.md`)
```
