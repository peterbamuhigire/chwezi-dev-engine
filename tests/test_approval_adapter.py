import json
import unittest
from pathlib import Path


class ApprovalAdapterTests(unittest.TestCase):
    def test_side_effecting_tool_actions_are_l3(self):
        payload = json.loads((Path(__file__).parents[1] / "docs" / "approval-adapter.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["engine"], "skills-web-dev")
        actions = {item["action_type"]: item for item in payload["actions"]}
        for action_type in ("shell.privileged.execute", "database.migration.apply", "deployment.production.release"):
            action = actions[action_type]
            self.assertEqual(action["class"], "L3")
            self.assertTrue(action["preview_required"] and action["idempotency_required"])
            self.assertTrue(action["rollback"] and action["verification"])


if __name__ == "__main__":
    unittest.main()
