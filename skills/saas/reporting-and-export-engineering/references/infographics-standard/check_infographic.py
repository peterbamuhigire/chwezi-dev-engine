#!/usr/bin/env python3
"""Checks for the Chwezi Infographics Design and Production Quality Standard 1.0.0.

Standard library only. Implements the calculations in references/mathematics-and-algorithms.md:
type size for a distance, print resolution, phone canvas text, lie factor, largest-remainder
rounding, contrast, ring radius, timeline spacing, the release score, and diagram structure checks
(flows, cycles, strict hierarchies) with a generated long text equivalent.

Usage:
  python check_infographic.py graph diagram.json      # structure checks; exit 1 on any failure
  python check_infographic.py describe diagram.json   # long text equivalent in step order
  python check_infographic.py size 1.0                # minimum pt for a 1 m reading distance
  python check_infographic.py ppi 0.5                 # required ppi at 0.5 m
  python check_infographic.py lie 3200000 3400000 0.2 0.4
  python check_infographic.py contrast "#1A6DB3" "#FFFFFF"
  python check_infographic.py shares 41.4 33.3 25.3

Diagram JSON: {"kind": "flow" | "cycle" | "tree",
               "nodes": [{"id": "S1", "label": "Mix", "type": "start|step|decision|end|exception",
                          "number": 1}],
               "edges": [{"from": "S1", "to": "S2", "label": "", "kind": "flow|feedback"}]}
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import deque
from difflib import SequenceMatcher

TAN_20_ARCMIN = math.tan(math.radians(20 / 60))
PT_PER_MM = 72 / 25.4


def min_type_pt(distance_m: float, arcmin: float = 20.0, cap: float = 0.70) -> float:
    """Minimum font size in points at actual print size for a reading distance (task 1)."""
    cap_mm = distance_m * 1000 * math.tan(math.radians(arcmin / 60))
    return cap_mm / cap * PT_PER_MM


def required_ppi(distance_m: float) -> float:
    """One pixel per arc-minute at the closest reading distance (task 2)."""
    return 1 / ((distance_m / 0.0254) * math.tan(math.radians(1 / 60)))


def effective_ppi(pixels: int, printed_mm: float) -> float:
    return pixels / (printed_mm / 25.4)


def canvas_text_px(min_css_px: float, canvas_px: float, slot_css_px: float) -> float:
    """Canvas pixels needed for text shown in a narrower slot (task 3)."""
    return min_css_px * canvas_px / slot_css_px


def lie_factor(data_a: float, data_b: float, shown_a: float, shown_b: float) -> float:
    """Effect shown divided by effect in the data (task 4); accept 0.95-1.05."""
    data_effect = abs(data_b - data_a) / abs(data_a)
    shown_effect = abs(shown_b - shown_a) / abs(shown_a)
    return shown_effect / data_effect


def largest_remainder(values: list[float], total: int = 100) -> list[int]:
    """Whole-number shares of `total` that always sum to it (task 4)."""
    s = sum(values)
    raw = [v * total / s for v in values]
    floors = [math.floor(r) for r in raw]
    spare = total - sum(floors)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - floors[i], reverse=True)
    for i in order[:spare]:
        floors[i] += 1
    return floors


def _linear(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast(fg: str, bg: str) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def ring_radius(n: int, width: float, gap: float) -> float:
    """Smallest ring radius so adjacent stages do not touch (task 6)."""
    return (width + gap) / (2 * math.sin(math.pi / n))


def timeline_errors(dates_days: list[float], positions: list[float]) -> list[float]:
    """Relative spacing error per segment against a linear time scale (task 7)."""
    scale = (positions[-1] - positions[0]) / (dates_days[-1] - dates_days[0])
    out = []
    for i in range(1, len(dates_days)):
        dt, dx = dates_days[i] - dates_days[i - 1], positions[i] - positions[i - 1]
        out.append(abs((dx / dt) / scale - 1) if dt else float("inf"))
    return out


WEIGHTS = {"accuracy": 25, "clarity": 20, "typography": 15, "hierarchy": 15,
           "accessibility": 10, "technical": 10, "brand": 5}


def release_score(ratings: dict[str, float]) -> float:
    """Weighted score from 0-1 ratings per dimension (task 11)."""
    return sum(WEIGHTS[k] * ratings[k] for k in WEIGHTS)


def _norm(label: str) -> str:
    label = re.sub(r"^\s*(step\s*)?\d+[.):-]?\s*", "", label.casefold())
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", label)).strip()


def check_graph(d: dict) -> list[str]:
    """Structure checks for flow, cycle and tree diagrams (task 5). Returns failures."""
    kind = d.get("kind", "flow")
    nodes, edges = d.get("nodes", []), d.get("edges", [])
    ids = [n["id"] for n in nodes]
    fails: list[str] = []
    if len(ids) != len(set(ids)):
        fails.append("duplicate node ids: " + ", ".join(sorted({i for i in ids if ids.count(i) > 1})))
    by_id = {n["id"]: n for n in nodes}
    for e in edges:
        for end in ("from", "to"):
            if e[end] not in by_id:
                fails.append(f"edge refers to unknown node {e[end]}")
    labels = [(n["id"], _norm(n.get("label", ""))) for n in nodes]
    for i, (a, la) in enumerate(labels):
        for b, lb in labels[i + 1:]:
            if la and lb and (la == lb or SequenceMatcher(None, la, lb).ratio() >= 0.9):
                fails.append(f"possible duplicate stage: {a} and {b}")
    out = {i: [] for i in ids}
    inn = {i: [] for i in ids}
    flow = [e for e in edges if e.get("kind", "flow") == "flow" and e["from"] in out and e["to"] in out]
    for e in edges:
        if e["from"] in out and e["to"] in out:
            out[e["from"]].append(e)
            inn[e["to"]].append(e)
    for i in ids:
        if not out[i] and not inn[i]:
            fails.append(f"orphan node {i}")
    if kind == "tree":
        roots = [i for i in ids if not inn[i]]
        if len(roots) != 1:
            fails.append(f"a strict hierarchy needs one root, found {len(roots)}")
        for i in ids:
            if len(inn[i]) > 1:
                fails.append(f"node {i} has {len(inn[i])} parents")
        if len(edges) != len(ids) - 1:
            fails.append("edges must equal nodes minus one in a strict hierarchy")
        if roots and len(_reach(roots[:1], out, "to")) != len(ids):
            fails.append("not every node is reachable from the root (cycle or split)")
        return fails
    if kind == "cycle":
        ring = [e for e in edges if e.get("kind", "flow") == "flow"]
        rout = {i: [e for e in ring if e["from"] == i] for i in ids}
        rin = {i: [e for e in ring if e["to"] == i] for i in ids}
        if any(len(rout[i]) != 1 or len(rin[i]) != 1 for i in ids):
            fails.append("every stage of a cycle needs exactly one ring edge in and one out")
        elif ids:
            seen, cur = [], ids[0]
            while cur not in seen:
                seen.append(cur)
                cur = rout[cur][0]["to"]
            if len(seen) != len(ids):
                fails.append("the ring does not visit every stage in one loop")
        if not any(n.get("type") == "start" for n in nodes):
            fails.append("a cycle needs a marked entry point (type start)")
        return fails
    starts = [n["id"] for n in nodes if n.get("type") == "start"] or [i for i in ids if not inn[i]]
    ends = [n["id"] for n in nodes if n.get("type") == "end"] or [i for i in ids if not out[i]]
    if not starts:
        fails.append("no start node")
    if not ends:
        fails.append("no end node")
    fwd = _reach(starts, out, "to")
    back = _reach(ends, inn, "from")
    for i in ids:
        if i not in fwd:
            fails.append(f"node {i} is not reachable from a start")
        if i not in back:
            fails.append(f"node {i} cannot reach an end (dead end)")
    for n in nodes:
        if n.get("type") == "decision":
            exits = out[n["id"]]
            if len(exits) < 2 or any(not e.get("label") for e in exits):
                fails.append(f"decision {n['id']} needs two or more labelled exits")
    order = _topo(ids, flow)
    if order is None:
        fails.append("flow edges contain a loop; mark real loops as kind feedback")
    else:
        numbers = [n["number"] for n in nodes if "number" in n]
        if len(numbers) != len(set(numbers)):
            fails.append("duplicate displayed step numbers")
        shown = [i for _, i in sorted((n["number"], n["id"]) for n in nodes if "number" in n)]
        if any(_path(b, a, flow) for a, b in zip(shown, shown[1:])):
            fails.append("displayed step numbers disagree with the process order")
    return fails


def _reach(seeds: list[str], adj: dict, key: str) -> set:
    seen, q = set(seeds), deque(seeds)
    while q:
        for e in adj[q.popleft()]:
            if e[key] not in seen:
                seen.add(e[key])
                q.append(e[key])
    return seen


def _topo(ids: list[str], flow: list[dict]) -> list[str] | None:
    indeg = {i: 0 for i in ids}
    for e in flow:
        indeg[e["to"]] += 1
    q = deque(i for i in ids if indeg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for e in flow:
            if e["from"] == i:
                indeg[e["to"]] -= 1
                if indeg[e["to"]] == 0:
                    q.append(e["to"])
    return order if len(order) == len(ids) else None


def _path(a: str, b: str, flow: list[dict]) -> bool:
    adj = {}
    for e in flow:
        adj.setdefault(e["from"], []).append(e["to"])
    seen, q = {a}, deque([a])
    while q:
        for nxt in adj.get(q.popleft(), []):
            if nxt == b:
                return True
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return False


def describe(d: dict) -> str:
    """Long text equivalent generated from the validated graph (INFO-A11Y-001)."""
    nodes = {n["id"]: n for n in d["nodes"]}
    flow = [e for e in d["edges"] if e.get("kind", "flow") == "flow"]
    order = _topo(list(nodes), flow) if d.get("kind", "flow") != "cycle" else list(nodes)
    lines = []
    for k, i in enumerate(order or list(nodes), 1):
        nxt = [f"{nodes[e['to']]['label']}" + (f" (if {e['label']})" if e.get("label") else "")
               for e in d["edges"] if e["from"] == i]
        tail = f" Next: {'; '.join(nxt)}." if nxt else " This is the end."
        lines.append(f"{k}. {nodes[i]['label']}.{tail}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, args = argv[1], argv[2:]
    if cmd in ("graph", "describe"):
        with open(args[0], encoding="utf-8") as fh:
            d = json.load(fh)
        if cmd == "describe":
            print(describe(d))
            return 0
        fails = check_graph(d)
        print("\n".join(fails) if fails else "structure: no failures")
        return 1 if fails else 0
    if cmd == "size":
        print(f"{min_type_pt(float(args[0])):.1f} pt")
    elif cmd == "ppi":
        print(f"{required_ppi(float(args[0])):.0f} ppi")
    elif cmd == "lie":
        lf = lie_factor(*map(float, args[:4]))
        print(f"lie factor {lf:.2f} ({'pass' if 0.95 <= lf <= 1.05 else 'FAIL'})")
        return 0 if 0.95 <= lf <= 1.05 else 1
    elif cmd == "contrast":
        print(f"{contrast(args[0], args[1]):.2f}:1")
    elif cmd == "shares":
        print(" ".join(map(str, largest_remainder([float(a) for a in args]))))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
