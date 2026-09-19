import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ai.shared_context import (  # noqa: E402
    ContextFact,
    ContextValidationError,
    SharedContextPacket,
    SourceRecord,
)


NOW = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)


def packet(**overrides):
    source = SourceRecord("SRC-1", "fixture://source-1", "tenant:A", "v1", NOW + timedelta(hours=1))
    fact = ContextFact("status", "ready", "SRC-1", "fixture://source-1", "tenant:A",
                       frozenset({"engineering"}), NOW + timedelta(hours=1))
    values = {"packet_id": "PKT-1", "objective": "ship fixture", "facts": (fact,),
              "relationships": (), "policy_version": "context-policy-1.0.0"}
    values.update(overrides)
    return SharedContextPacket.create(**values), {"SRC-1": source}


class SharedContextTests(unittest.TestCase):
    def test_valid_packet_has_replayable_hash_and_snapshot(self):
        context, sources = packet()
        context.require_valid("ship fixture", sources, {"engineering"}, NOW)
        self.assertEqual(context.render_snapshot(), context.render_snapshot())
        self.assertEqual(len(context.packet_hash), 64)

    def test_stale_mismatched_missing_and_revoked_context_block(self):
        context, sources = packet(objective="other objective")
        findings = context.validate("ship fixture", sources, {"engineering"}, NOW)
        self.assertIn("MISMATCHED_OBJECTIVE", {item.code for item in findings})
        stale, stale_sources = packet()
        stale_fact = ContextFact("status", "old", "SRC-1", "fixture://source-1", "tenant:A",
                                 frozenset({"engineering"}), NOW - timedelta(seconds=1))
        stale = SharedContextPacket.create("PKT-2", "ship fixture", (stale_fact,))
        stale_codes = {item.code for item in stale.validate("ship fixture", stale_sources, {"engineering"}, NOW)}
        self.assertIn("STALE_CONTEXT", stale_codes)
        missing = SharedContextPacket.create("PKT-3", "ship fixture", (
            ContextFact("status", "x", "MISSING", "fixture://missing", "tenant:A", frozenset({"engineering"})),))
        self.assertIn("MISSING_SOURCE", {item.code for item in missing.validate("ship fixture", {}, {"engineering"}, NOW)})
        revoked = SharedContextPacket.create("PKT-4", "ship fixture", (
            ContextFact("status", "x", "SRC-1", "fixture://source-1", "tenant:A", frozenset({"finance"})),))
        self.assertIn("REVOKED_ACCESS", {item.code for item in revoked.validate("ship fixture", sources, {"engineering"}, NOW)})

    def test_require_valid_raises_with_named_finding(self):
        context, sources = packet(objective="wrong")
        with self.assertRaisesRegex(ContextValidationError, "MISMATCHED_OBJECTIVE"):
            context.require_valid("ship fixture", sources, {"engineering"}, NOW)


if __name__ == "__main__":
    unittest.main()
