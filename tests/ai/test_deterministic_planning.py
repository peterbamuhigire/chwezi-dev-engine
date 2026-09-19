import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ai.deterministic_planning import DeterministicPlanner  # noqa: E402


GRAPH = {"A": ("B", "C"), "B": ("D",), "C": ("D",), "D": ()}
COSTS = {("A", "B"): 1, ("A", "C"): 1, ("B", "D"): 2, ("C", "D"): 2}


class DeterministicPlanningTests(unittest.TestCase):
    def test_known_optimum_is_legal_and_stable(self):
        planner = DeterministicPlanner()
        result = planner.plan("A", lambda node: node == "D", lambda node: GRAPH[node],
                              lambda left, right: COSTS[(left, right)], lambda _node: 0)
        self.assertEqual(result.status, "planned")
        self.assertEqual(result.path, ("A", "B", "D"))
        self.assertEqual(result.cost, 3)
        self.assertEqual(result, planner.plan("A", lambda node: node == "D", lambda node: GRAPH[node],
                                              lambda left, right: COSTS[(left, right)], lambda _node: 0))

    def test_negative_cost_invalid_edge_impossible_goal_and_budget_are_explicit(self):
        planner = DeterministicPlanner()
        negative = planner.plan("A", lambda node: node == "D", lambda _node: ("D",), lambda _l, _r: -1)
        self.assertEqual((negative.status, negative.reason), ("rejected", "negative_cost"))
        invalid = planner.plan("A", lambda node: node == "D", lambda _node: (None,), lambda _l, _r: 1)
        self.assertEqual((invalid.status, invalid.reason), ("rejected", "invalid_edge"))
        impossible = planner.plan("A", lambda node: node == "Z", lambda node: GRAPH[node], lambda _l, _r: 1)
        self.assertEqual(impossible.status, "no_plan")
        budget = planner.plan("A", lambda node: node == "D", lambda node: GRAPH[node],
                              lambda _l, _r: 1, max_expansions=1)
        self.assertEqual(budget.status, "budget_exhausted")


if __name__ == "__main__":
    unittest.main()
