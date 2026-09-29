"""Synthetic token settings for the fixture. The keys are test values, not secrets."""
ISSUER = "https://id.k.example"
AUDIENCE = "k-exports"
KEYS = {
    "k1": b"synthetic-signing-key-one-0000000",
    "k2": b"synthetic-signing-key-two-0000000",
}
ACTIVE_KID = "k1"
TOKEN_TTL_SECONDS = 900
