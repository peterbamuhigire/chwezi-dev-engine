"""Bounded, deterministic A* planning with no side effects."""
from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
from typing import Callable, Iterable


class PlanningError(ValueError):
    """Raised for malformed planner inputs."""


@dataclass(frozen=True)
class PlanResult:
    status: str
    path: tuple[str, ...] = ()
    cost: float | None = None
    expanded_nodes: int = 0
    reason: str | None = None


class DeterministicPlanner:
    """A pure planner over string nodes; it never invokes an action executor."""

    def plan(self, start: str, is_goal: Callable[[str], bool],
             neighbours: Callable[[str], Iterable[str]],
             cost: Callable[[str, str], float],
             heuristic: Callable[[str], float] | None = None,
             max_expansions: int = 1000) -> PlanResult:
        if not isinstance(start, str) or not start:
            raise PlanningError("start must be a non-empty string")
        if not callable(is_goal) or not callable(neighbours) or not callable(cost):
            raise PlanningError("goal, neighbours and cost must be callable")
        if heuristic is not None and not callable(heuristic):
            raise PlanningError("heuristic must be callable or None")
        if not isinstance(max_expansions, int) or max_expansions < 0:
            raise PlanningError("max_expansions must be a non-negative integer")
        estimate = heuristic or (lambda _node: 0.0)
        try:
            start_h = self._number(estimate(start), "heuristic")
        except (TypeError, ValueError) as exc:
            raise PlanningError(str(exc)) from exc
        if start_h < 0:
            return PlanResult("rejected", reason="negative_heuristic")
        queue: list[tuple[float, float, str, tuple[str, ...]]] = [(start_h, 0.0, start, (start,))]
        best: dict[str, float] = {start: 0.0}
        expanded = 0
        while queue:
            f_score, current_cost, node, path = heapq.heappop(queue)
            if current_cost != best.get(node):
                continue
            try:
                goal_reached = bool(is_goal(node))
            except Exception as exc:
                return PlanResult("rejected", expanded_nodes=expanded,
                                  reason=f"invalid_goal: {type(exc).__name__}")
            if goal_reached:
                return PlanResult("planned", path, current_cost, expanded)
            if expanded >= max_expansions:
                return PlanResult("budget_exhausted", expanded_nodes=expanded,
                                  reason="max_expansions reached")
            expanded += 1
            try:
                raw_neighbours = list(neighbours(node))
            except Exception as exc:
                return PlanResult("rejected", expanded_nodes=expanded,
                                  reason=f"invalid_edges: {type(exc).__name__}")
            if any(not isinstance(child, str) or not child for child in raw_neighbours):
                return PlanResult("rejected", expanded_nodes=expanded, reason="invalid_edge")
            for child in sorted(raw_neighbours):
                try:
                    edge_cost = self._number(cost(node, child), "cost")
                except Exception as exc:
                    return PlanResult("rejected", expanded_nodes=expanded, reason=str(exc))
                if edge_cost < 0:
                    return PlanResult("rejected", expanded_nodes=expanded, reason="negative_cost")
                candidate = current_cost + edge_cost
                if candidate >= best.get(child, math.inf):
                    continue
                try:
                    child_h = self._number(estimate(child), "heuristic")
                except Exception as exc:
                    return PlanResult("rejected", expanded_nodes=expanded, reason=str(exc))
                if child_h < 0:
                    return PlanResult("rejected", expanded_nodes=expanded, reason="negative_heuristic")
                best[child] = candidate
                heapq.heappush(queue, (candidate + child_h, candidate, child, path + (child,)))
        return PlanResult("no_plan", expanded_nodes=expanded, reason="goal is unreachable")

    @staticmethod
    def _number(value: float, label: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise PlanningError(f"{label} must be a finite number")
        return float(value)
