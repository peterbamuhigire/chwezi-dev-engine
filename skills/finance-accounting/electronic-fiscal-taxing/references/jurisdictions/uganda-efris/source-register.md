# Uganda EFRIS Engineering Source Register

Accessed 2026-08-28. This register is a synthesis index, not production
approval. Promote each technical fact into the consuming project register with
named verifier, exact version/date, archive evidence, and test coverage.

## Supplied documents

| ID | Supplied material | Engineering use | State |
|---|---|---|---|
| U-1 | EFRIS Interface User Requirement Specifications (Business Requirements) v1.5 | document content, print, communication, reports | supplied/versioned; currentness required |
| U-2 | Interface Design for EFRIS v24.0.1 URA | envelope, T101-T144 family, fields and responses | supplied technical pack; confirm current |
| U-3 | How to use the System to System API V3 | registration, T101/T104, security narrative | supplied guide; older/conflicting details possible |
| U-4 | Step by step guide on how to integrate System2system on EFRIS | onboarding, UAT, migration | supplied guide; verify with URA |
| U-5 | EFRIS Offline Mode Enabler Requirements | offline topology and limits | supplied requirements; verify |
| U-6 | EFRIS Offline-Mode Enabler Installation Guide v1.6 | installation/runtime/ports | supplied guide; do not freeze versions blindly |
| U-7 | Step by step guide for EFRIS device and thumbprint registration | device/certificate operations | supplied guide; approval required |
| U-8 | EFRIS Taxpayers Training Material v2 | portal, catalogue, stock, documents, reports | supplied training material |

## Public URA sources

- `https://ura.go.ug/en/efris/` — channel, registration, FDN/verification/QR,
  public offline guidance; current public check 2026-08-28.
- `https://ura.go.ug/en/efris-handbook/` — taxpayer workflow and public
  concepts; current public check 2026-08-28.
- `https://ura.go.ug/en/efris/efris-registration/` — registration sequence;
  current public check 2026-08-28.

## Production blockers

The public pages do not publish the complete authenticated S2S contract. Do not
activate production until BIRDC has the current URA endpoint, environment,
interface version, request/response schema, cryptographic/key procedure,
device/profile registration, UAT approval, and offline/manual exception rules.

The supplied material differs on labels such as `AP04`/`APP04`, versions,
endpoints, algorithms, and legal references. Preserve the original source and
make the conflict explicit; do not silently select one value.
