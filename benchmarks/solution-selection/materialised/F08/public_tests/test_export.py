import unittest

from app.errors import Denied
from app.export_jobs import enqueue_export, run_export
from app.read_api import read_document
from public_tests.helpers import build


class ExportTests(unittest.TestCase):
    def test_exporter_exports_own_tenant_document(self):
        ctx, idp = build()
        token = idp.issue_token("amina", ctx.now())
        job = enqueue_export(ctx, token, "doc-100")
        run_export(ctx, job)
        self.assertIn("Tenant A body", ctx.exports[job])

    def test_cross_tenant_export_is_denied(self):
        ctx, idp = build()
        token = idp.issue_token("amina", ctx.now())
        with self.assertRaises(Denied):
            enqueue_export(ctx, token, "doc-200")

    def test_missing_token_is_denied(self):
        ctx, idp = build()
        with self.assertRaises(Denied):
            enqueue_export(ctx, None, "doc-100")

    def test_read_api_is_tenant_scoped(self):
        ctx, idp = build()
        token = idp.issue_token("amina", ctx.now())
        self.assertEqual(read_document(ctx, token, "doc-100")["title"], "Q3 plan")
        with self.assertRaises(Denied):
            read_document(ctx, token, "doc-200")


if __name__ == "__main__":
    unittest.main()
