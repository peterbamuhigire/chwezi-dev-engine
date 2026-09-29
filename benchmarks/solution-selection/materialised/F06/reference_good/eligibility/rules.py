"""Eligibility rules for loans, youth grants and co-operative membership.

Public behaviour is pinned: return values, exception types and messages, and the exact order
of audit events are relied on by callers and by compliance tooling.

Each product runs the shared opening checks (request audit, evaluate permission, integer age)
and then its own policy steps in its own order. The order is data in each function, not a
shared pipeline, because the products deliberately differ (membership screens sanctions before
residency; grants require a regional delegation, a separate trust boundary from the evaluate
permission).
"""
from __future__ import annotations

from .audit import AuditLog
from .errors import IneligibleApplicant, InvalidApplicant, PermissionDenied
from .models import Actor, Applicant

EVALUATE = "eligibility.evaluate"
EAST_AFRICAN_COMMUNITY = ("UG", "KE", "TZ", "RW")


def _open_request(product: str, applicant: Applicant, actor: Actor, audit: AuditLog) -> None:
    audit.record(f"{product}.requested", applicant.id)
    if not actor.has_permission(EVALUATE):
        audit.record(f"{product}.denied.permission", actor.id)
        raise PermissionDenied(f"actor lacks {EVALUATE}")
    if not isinstance(applicant.age, int) or isinstance(applicant.age, bool):
        raise InvalidApplicant("age must be an integer")


def _reject(product: str, reason: str, message: str, applicant: Applicant, audit: AuditLog) -> None:
    audit.record(f"{product}.ineligible.{reason}", applicant.id)
    raise IneligibleApplicant(message)


def _require_minimum_age(product: str, minimum: int, applicant: Applicant, audit: AuditLog) -> None:
    if applicant.age < minimum:
        _reject(product, "age", f"applicant is under {minimum}", applicant, audit)


def _require_not_sanctioned(product: str, applicant: Applicant, audit: AuditLog) -> None:
    if applicant.sanctioned:
        _reject(product, "sanctions", "applicant is on the sanctions list", applicant, audit)


def _require_resident(product: str, applicant: Applicant, audit: AuditLog) -> None:
    if applicant.country != "UG":
        _reject(product, "residency", "applicant is not resident", applicant, audit)


def _eligible(product: str, applicant: Applicant, audit: AuditLog, **details: object) -> dict:
    audit.record(f"{product}.eligible", applicant.id)
    return {"product": product, "eligible": True, **details}


def check_loan_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _open_request("loan", applicant, actor, audit)
    _require_minimum_age("loan", 18, applicant, audit)
    _require_resident("loan", applicant, audit)
    _require_not_sanctioned("loan", applicant, audit)
    if applicant.monthly_income < 500_000:
        _reject("loan", "income", "income below loan threshold", applicant, audit)
    tier = "premium" if applicant.monthly_income >= 2_000_000 else "standard"
    return _eligible("loan", applicant, audit, tier=tier)


def check_grant_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _open_request("grant", applicant, actor, audit)
    _require_minimum_age("grant", 18, applicant, audit)
    if applicant.age > 35:
        _reject("grant", "age", "applicant is over 35", applicant, audit)
    _require_resident("grant", applicant, audit)
    # Separate trust boundary: the evaluate permission is not enough for grants; the actor
    # also needs a delegation for the applicant's region. Do not merge this into the opening
    # permission check.
    if not actor.can_act_for(applicant.region):
        audit.record("grant.denied.region", actor.id)
        raise PermissionDenied("actor has no delegation for this region")
    _require_not_sanctioned("grant", applicant, audit)
    return _eligible("grant", applicant, audit, region=applicant.region)


def check_membership_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _open_request("membership", applicant, actor, audit)
    _require_minimum_age("membership", 16, applicant, audit)
    _require_not_sanctioned("membership", applicant, audit)  # sanctions before residency, by policy
    if applicant.country not in EAST_AFRICAN_COMMUNITY:
        _reject("membership", "residency", "applicant is not resident in the region", applicant, audit)
    band = "youth" if applicant.age < 25 else "adult"
    return _eligible("membership", applicant, audit, band=band)
