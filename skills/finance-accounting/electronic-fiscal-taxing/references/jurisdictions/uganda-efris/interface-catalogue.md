# Uganda EFRIS Interface Catalogue

This catalogue is intentionally a versioned implementation map from the
provided technical documents. Interface codes and fields must be confirmed
against the current URA pack before code constants are frozen.

## Capability groups

| Group | Supplied examples | Integration use |
|---|---|---|
| Session/key/system | T101 time, T103 parameters/login, T104 key, T115 dictionaries | clock, key/cache, configuration and lookup refresh |
| Taxpayer/master | T119 taxpayer, T123/T124 categories/commodities, T125 excise, T126 FX | seller/buyer/catalogue/tax readiness |
| Goods/stock | T127 goods, T128 stock, T130 upload, T131 maintain, T139 transfer | product identity and stock synchronisation |
| Sales documents | T109 upload, T106/T107 query, T108 detail | issue/query/verify fiscal document |
| Corrections | T110 apply credit/debit, T111 status, T112 detail, T113 approve, T114 cancel | controlled correction lifecycle |
| Special reports | T137 exemption/deemed and other versioned capabilities | special treatment only when verified |

## T109 mapping shape

The supplied v24 design groups the upload around seller details, basic
information, buyer, goods, tax details, summary, payment, and extension/reason
fields. The adapter should construct these from a canonical invoice snapshot,
including seller/TIN/branch/device, internal reference, customer identity,
product code/UOM, quantity/price/discount, tax category, currency, payment,
and correction linkage.

The response must persist the authority identifiers and complete redacted
evidence before the ERP marks the document accepted. Product/category/UOM
identifiers must be mapped from synchronised authority master data.

## T110 and corrections

Credit/debit workflows need original-document identity, reason, line/tax
adjustment, approval/status handling, and linked accounting correction. B2B/B2G
approval and non-TIN cases are version-sensitive; keep them in a capability
matrix and fail closed when the current rule is unknown.

## Versioning

Keep a provider contract version and dictionary versions with every payload. A
new provider version is tested in parallel; do not mutate a frozen response
parser without contract evidence and consumer compatibility review.
