"""Eligibility rules for loans, youth grants and co-operative membership.

Public behaviour is pinned: return values, exception types and messages, and the exact order
of audit events are relied on by callers and by compliance tooling.
"""
from __future__ import annotations

from .audit import AuditLog
from .errors import IneligibleApplicant, InvalidApplicant, PermissionDenied
from .models import Actor, Applicant


def check_loan_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    audit.record("loan.requested", applicant.id)
    if not actor.has_permission("eligibility.evaluate"):
        audit.record("loan.denied.permission", actor.id)
        raise PermissionDenied("actor lacks eligibility.evaluate")
    if not isinstance(applicant.age, int) or isinstance(applicant.age, bool):
        raise InvalidApplicant("age must be an integer")
    if applicant.age < 18:
        audit.record("loan.ineligible.age", applicant.id)
        raise IneligibleApplicant("applicant is under 18")
    if applicant.country != "UG":
        audit.record("loan.ineligible.residency", applicant.id)
        raise IneligibleApplicant("applicant is not resident")
    if applicant.sanctioned:
        audit.record("loan.ineligible.sanctions", applicant.id)
        raise IneligibleApplicant("applicant is on the sanctions list")
    if applicant.monthly_income < 500_000:
        audit.record("loan.ineligible.income", applicant.id)
        raise IneligibleApplicant("income below loan threshold")
    tier = "premium" if applicant.monthly_income >= 2_000_000 else "standard"
    audit.record("loan.eligible", applicant.id)
    return {"product": "loan", "eligible": True, "tier": tier}


def check_grant_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    audit.record("grant.requested", applicant.id)
    if not actor.has_permission("eligibility.evaluate"):
        audit.record("grant.denied.permission", actor.id)
        raise PermissionDenied("actor lacks eligibility.evaluate")
    if not isinstance(applicant.age, int) or isinstance(applicant.age, bool):
        raise InvalidApplicant("age must be an integer")
    if applicant.age < 18:
        audit.record("grant.ineligible.age", applicant.id)
        raise IneligibleApplicant("applicant is under 18")
    if applicant.age > 35:
        audit.record("grant.ineligible.age", applicant.id)
        raise IneligibleApplicant("applicant is over 35")
    if applicant.country != "UG":
        audit.record("grant.ineligible.residency", applicant.id)
        raise IneligibleApplicant("applicant is not resident")
    if not actor.has_permission("eligibility.evaluate") or not actor.can_act_for(applicant.region):
        audit.record("grant.denied.region", actor.id)
        raise PermissionDenied("actor has no delegation for this region")
    if applicant.sanctioned:
        audit.record("grant.ineligible.sanctions", applicant.id)
        raise IneligibleApplicant("applicant is on the sanctions list")
    audit.record("grant.eligible", applicant.id)
    return {"product": "grant", "eligible": True, "region": applicant.region}


def check_membership_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    audit.record("membership.requested", applicant.id)
    if not actor.has_permission("eligibility.evaluate"):
        audit.record("membership.denied.permission", actor.id)
        raise PermissionDenied("actor lacks eligibility.evaluate")
    if not isinstance(applicant.age, int) or isinstance(applicant.age, bool):
        raise InvalidApplicant("age must be an integer")
    if applicant.age < 16:
        audit.record("membership.ineligible.age", applicant.id)
        raise IneligibleApplicant("applicant is under 16")
    if applicant.sanctioned:
        audit.record("membership.ineligible.sanctions", applicant.id)
        raise IneligibleApplicant("applicant is on the sanctions list")
    if applicant.country not in ("UG", "KE", "TZ", "RW"):
        audit.record("membership.ineligible.residency", applicant.id)
        raise IneligibleApplicant("applicant is not resident in the region")
    band = "youth" if applicant.age < 25 else "adult"
    audit.record("membership.eligible", applicant.id)
    return {"product": "membership", "eligible": True, "band": band}
