# Natural synthetic seeding content rule

Date: 2026-08-20

Updated `skills/saas/full-coverage-saas-seeding` to require natural, culturally appropriate human-facing seed content without `DEMO`, `TEST`, `SAMPLE`, placeholder prose, or gibberish in names, titles, descriptions, complaints, notes, and narratives.

Sensitive values that could be mistaken for authentic legal, regulatory, identity, tax, or financial identifiers must contain the literal marker `DEMO`. A seeder must use an approved sandbox identifier contract or stop with `BLOCKED_CAPABILITY` when an ordinary validator cannot accept that marker. It may not generate a realistic unmarked substitute.

Technical fixture keys and manifest-only ownership markers may retain `DEMO`, but must not render as business content. Contract-test cases now cover both rules.
