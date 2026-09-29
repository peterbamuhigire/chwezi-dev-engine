"""Value objects passed to the eligibility rules."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Actor:
    id: str
    permissions: frozenset[str] = field(default_factory=frozenset)
    regions: frozenset[str] = field(default_factory=frozenset)

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def can_act_for(self, region: str) -> bool:
        return region in self.regions


@dataclass(frozen=True)
class Applicant:
    id: str
    age: object
    country: str
    sanctioned: bool
    monthly_income: int
    region: str
