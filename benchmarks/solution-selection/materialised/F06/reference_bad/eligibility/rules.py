"""Eligibility rules for loans, youth grants and co-operative membership.

Refactored: the three products share one common pipeline of checks.
"""
from __future__ import annotations

from .audit import AuditLog
from .errors import IneligibleApplicant, InvalidApplicant, PermissionDenied
from .models import Actor, Applicant


def _common_checks(product, applicant, actor, audit, min_age, countries, residency_message):
    audit.record(f"{product}.requested", applicant.id)
    if not actor.has_permission("eligibility.evaluate"):
        audit.record(f"{product}.denied.permission", actor.id)
        raise PermissionDenied("actor lacks eligibility.evaluate")
    if not isinstance(applicant.age, int) or isinstance(applicant.age, bool):
        raise InvalidApplicant("age must be an integer")
    if applicant.age < min_age:
        audit.record(f"{product}.ineligible.age", applicant.id)
        raise IneligibleApplicant(f"applicant is under {min_age}")
    if applicant.country not in countries:
        audit.record(f"{product}.ineligible.residency", applicant.id)
        raise IneligibleApplicant(residency_message)
    if applicant.sanctioned:
        audit.record(f"{product}.ineligible.sanctions", applicant.id)
        raise IneligibleApplicant("applicant is on the sanctions list")


def check_loan_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _common_checks("loan", applicant, actor, audit, 18, ("UG",), "applicant is not resident")
    if applicant.monthly_income < 500_000:
        audit.record("loan.ineligible.income", applicant.id)
        raise IneligibleApplicant("income below loan threshold")
    tier = "premium" if applicant.monthly_income >= 2_000_000 else "standard"
    audit.record("loan.eligible", applicant.id)
    return {"product": "loan", "eligible": True, "tier": tier}


def check_grant_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _common_checks("grant", applicant, actor, audit, 18, ("UG",), "applicant is not resident")
    if applicant.age > 35:
        audit.record("grant.ineligible.age", applicant.id)
        raise IneligibleApplicant("applicant is over 35")
    # The second permission check was redundant: permission is already verified above.
    audit.record("grant.eligible", applicant.id)
    return {"product": "grant", "eligible": True, "region": applicant.region}


def check_membership_eligibility(applicant: Applicant, actor: Actor, audit: AuditLog) -> dict:
    _common_checks("membership", applicant, actor, audit, 16, ("UG", "KE", "TZ", "RW"), "applicant is not resident in the region")
    band = "youth" if applicant.age < 25 else "adult"
    audit.record("membership.eligible", applicant.id)
    return {"product": "membership", "eligible": True, "band": band}
