from app.context import AppContext
from app.documents import Repository
from app.identity import FakeIdentityProvider

SECRET = b"fixture-signing-key-not-for-production"


def build():
    idp = FakeIdentityProvider(SECRET)
    idp.add_user("amina", "tenant-a", {"reader", "exporter"})
    idp.add_user("brian", "tenant-b", {"reader", "exporter"})
    idp.add_user("carol", "tenant-a", {"reader"})
    repo = Repository()
    repo.add("doc-100", "tenant-a", "Q3 plan", "Tenant A body")
    repo.add("doc-200", "tenant-b", "Board pack", "Tenant B body")
    return AppContext(SECRET, idp, repo), idp
