# Export Format Spec - Reference

The right to data portability (GDPR Art.20, and equivalents under POPIA, Uganda DPPA, Kenya DPA, CCPA) requires delivering the data subject's data in a "structured, commonly used, machine-readable format". This reference specifies the export package: its layout, the per-data-type format choices, the completeness rules, and the integrity manifest that lets the recipient verify the package was not truncated or tampered with. An export that is a single opaque blob, or that silently omits half the data, satisfies the letter of nothing.

## section 1 Package Layout

The export is a single archive (`.zip` or `.tar.gz`) with a fixed, self-describing structure.

```text
export_tenant-123_2026-05-30.zip
+-- README.md                 # human-readable: what this is, how to read it
+-- manifest.json             # machine-readable index + integrity (section 5)
+-- metadata.json             # request context: who, when, scope, regulation
+-- data/
|   +-- users.jsonl           # one JSON object per line, schema-tagged
|   +-- projects.jsonl
|   +-- messages.jsonl
|   +-- settings.json         # single object
|   +-- audit_subset.jsonl    # the subject's OWN actions only
+-- files/
|   +-- <original-folder-structure-preserved>
+-- schemas/
|   +-- users.schema.json     # JSON Schema for each data file
|   +-- projects.schema.json
+-- NOT_INCLUDED.md           # what was withheld and the lawful basis (section 4)
```

The layout is identical for user-level and tenant-level exports; only the scope (in `metadata.json`) and volume differ.

## section 2 Format Choice Per Data Type

| Data type | Format | Why; failure mode of the wrong choice |
|---|---|---|
| Tabular records (users, rows) | JSON Lines (`.jsonl`) | Streamable for large tenants; one object per line. A single giant JSON array must be fully parsed in memory - it OOMs the recipient on a big tenant |
| Tabular, also offered for spreadsheets | CSV alongside JSONL | Non-technical subjects open CSV; CSV alone loses nested structure and types |
| Nested config / preferences | JSON | Preserves structure; CSV would flatten and lose meaning |
| Linked/graph data (relationships) | JSON-LD with `@context` | Self-describing semantics; plain JSON loses the meaning of foreign keys |
| Binary content (uploads, images) | Original files, folder structure preserved | Re-encoding corrupts; base64-in-JSON bloats 33% and is unusable |
| Timestamps | ISO 8601 UTC (`2026-05-30T14:12:00Z`) | Locale-formatted dates are ambiguous and non-portable |
| Identifiers | Stable opaque ids + a human label where one exists | Raw internal sequence ids alone are meaningless to the subject |

Default to JSONL for tabular data with JSON Schema in `schemas/`, and offer CSV as a convenience copy for the largest, flattest tables.

## section 3 Schema and Field Documentation

Machine-readable is necessary but not sufficient; the recipient must understand the fields.

- Each `data/*.jsonl` file has a corresponding `schemas/<name>.schema.json` (JSON Schema draft 2020-12) describing every field, type, and whether nullable.
- `README.md` documents, in plain language, what each file contains and what the non-obvious fields mean.
- Enumerated values are explained (a `status` field lists its possible values and their meaning).
- Foreign-key-style references between files are documented so the recipient can rejoin them.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "users",
  "type": "object",
  "properties": {
    "user_id":    {"type": "string", "description": "Stable opaque user identifier"},
    "email":      {"type": "string", "format": "email"},
    "created_at": {"type": "string", "format": "date-time", "description": "ISO 8601 UTC"},
    "role":       {"type": "string", "enum": ["owner", "admin", "member"]}
  },
  "required": ["user_id", "email", "created_at"]
}
```

## section 4 Completeness

The export must contain all of the subject's personal data within scope, and must be explicit about anything withheld.

- **Inclusion rule**: every store that holds the subject's PII (per the data-store inventory in the parent skill) contributes to the export, or is explicitly listed in `NOT_INCLUDED.md` with the reason.
- **Scope**: a user-level export contains that user's data across the tenants where they appear; a tenant-level export contains the whole organisation's data. `metadata.json` records which.
- **`NOT_INCLUDED.md`** lists, for each withheld category, the lawful basis: financial records retained for tax law, audit-log entries retained for SOC2 (and pseudonymised), other data subjects' PII excluded to protect their rights, trade-secret-derived data, and so on. Silent omission is the failure mode - the subject cannot tell whether data is missing because it does not exist or because you forgot it.
- **Derived data**: where a derived store (search, warehouse) holds copies, the export draws from the authoritative source, not the derived copy, to avoid stale or partial data.

## section 5 Integrity Manifest

The recipient must be able to verify the package is complete and untampered. `manifest.json` provides per-file checksums and the totals.

```json
{
  "export_id": "exp_8821",
  "tenant_id": "123",
  "scope": "tenant",
  "generated_at": "2026-05-30T14:12:00Z",
  "regulation": ["GDPR", "Uganda-DPPA"],
  "files": [
    {"path": "data/users.jsonl",    "bytes": 184320, "records": 412,  "sha256": "9f86d0...c1d2"},
    {"path": "data/projects.jsonl", "bytes": 922011, "records": 1880, "sha256": "a3f1bb...77ee"},
    {"path": "files/logo.png",      "bytes": 20481,  "sha256": "44ce8a...90b1"}
  ],
  "totals": {"files": 3, "bytes": 1126812, "records": 2292},
  "manifest_sha256": "self-excluded; sign separately",
  "signature": "ed25519:base64-signature-over-manifest"
}
```

- Each file lists byte size, record count (for line-based files), and a SHA-256 digest. The recipient recomputes and compares - a mismatch means truncation or tampering.
- The manifest itself is signed (for example Ed25519) by the platform's export key so the recipient can confirm provenance.
- `records` per file plus `totals` let the recipient detect a truncated transfer that a naive "the ZIP opened fine" check would miss.

The wrong choice - no manifest - means a half-downloaded or corrupted export is indistinguishable from a complete one, and the subject builds on incomplete data without knowing.

## section 6 Delivery and Security

- Upload to a private bucket; deliver via a signed URL with a short expiry (for example 7 days).
- Send the link only to the verified email on file (see `requester-verification.md`), never to a newly supplied address.
- The export contains PII: encrypt at rest, log the generation and each download in the audit log, and expire and delete the artifact after the download window.
- For high-sensitivity exports, optionally encrypt the archive and deliver the passphrase out of band.

## section 7 Time and Scale

- GDPR allows 30 days; aim for hours to days. For large tenants, the job is queued and batched (stream JSONL rather than buffering whole tables in memory).
- The export job is tracked in an `exports` table with status (`queued`, `running`, `ready`, `delivered`, `expired`) and is itself audited.

## section 7a Verifying a Received Export

The recipient (or your own QA before delivery) verifies completeness and integrity from the manifest:

```python
import hashlib, json

def verify_export(root):
    manifest = json.load(open(f"{root}/manifest.json"))
    seen_bytes = 0
    for entry in manifest["files"]:
        data = open(f"{root}/{entry['path']}", "rb").read()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == entry["sha256"], f"checksum mismatch: {entry['path']}"
        assert len(data) == entry["bytes"], f"size mismatch: {entry['path']}"
        if entry["path"].endswith(".jsonl"):
            lines = data.decode().splitlines()
            assert len(lines) == entry["records"], f"record count mismatch: {entry['path']}"
        seen_bytes += len(data)
    assert seen_bytes == manifest["totals"]["bytes"], "total bytes mismatch"
    # then verify the manifest signature with the platform's public key
    return "ok"
```

A truncated transfer fails the size or record-count assertion; a tampered file fails the checksum; a forged package fails the signature check. Running this as a pre-delivery gate means you never hand a customer a silently corrupt export.

## section 7b Sample README Contents

The bundle's `README.md` is the human entry point and should answer, in plain language:

```text
- What this archive is (a data export for <tenant/user>, generated <date>, under <regulation>).
- How to read it: data/ holds your records as JSON Lines (one record per line);
  files/ holds your uploaded files in their original folders; schemas/ describes each field.
- What is NOT here and why: see NOT_INCLUDED.md (financial records retained for tax law, etc.).
- How to verify integrity: see manifest.json; each file lists a SHA-256 checksum.
- Who to contact (DPO / support) with questions about this export.
```

A bundle that is machine-readable but ships with no README forces the subject to reverse-engineer your schema - technically compliant, practically useless, and a likely complaint to the supervisory authority.

## section 8 Anti-Patterns

- **Single opaque blob** (a raw DB dump) - not "commonly used"; the subject cannot read it.
- **One giant JSON array** instead of JSONL - OOMs the recipient on a large tenant.
- **PDF as the only format** - human-readable but not machine-readable; fails portability.
- **No schema / field docs** - machine-readable bytes nobody can interpret.
- **Silent omission** - withheld data not declared in `NOT_INCLUDED.md`; subject cannot tell what is missing.
- **No integrity manifest** - truncation and tampering undetectable.
- **base64 binaries inside JSON** - 33% bloat, unusable files.
- **Delivering to an unverified address** - hands the subject's data to whoever asked.
- **Export link with no expiry** - PII archive sits behind a forever-live URL.

## See Also

- `saas-tenant-data-portability-and-erasure` section 4 (export workflow), section 6 (verification).
- `references/requester-verification.md` - who is allowed to receive an export.
- `references/erasure-cascade.md` - the final export offered before erasure.
- `uganda-dppa-compliance` - regional portability obligations.
