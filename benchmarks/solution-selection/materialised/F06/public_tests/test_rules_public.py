import unittest

from eligibility import check_grant_eligibility, check_loan_eligibility, check_membership_eligibility
from eligibility.audit import AuditLog
from eligibility.errors import IneligibleApplicant, PermissionDenied
from eligibility.models import Actor, Applicant

OFFICER = Actor("officer-1", frozenset({"eligibility.evaluate"}), frozenset({"central"}))


def applicant(**overrides):
    base = dict(id="app-1", age=30, country="UG", sanctioned=False, monthly_income=800_000, region="central")
    base.update(overrides)
    return Applicant(**base)


class PublicRuleTests(unittest.TestCase):
    def test_standard_loan(self):
        audit = AuditLog()
        self.assertEqual(check_loan_eligibility(applicant(), OFFICER, audit), {"product": "loan", "eligible": True, "tier": "standard"})
        self.assertEqual(audit.events, [("loan.requested", "app-1"), ("loan.eligible", "app-1")])

    def test_premium_loan(self):
        self.assertEqual(check_loan_eligibility(applicant(monthly_income=2_500_000), OFFICER, AuditLog())["tier"], "premium")

    def test_grant_with_delegation(self):
        self.assertEqual(check_grant_eligibility(applicant(age=24), OFFICER, AuditLog())["region"], "central")

    def test_membership_band(self):
        self.assertEqual(check_membership_eligibility(applicant(age=19, country="KE"), OFFICER, AuditLog())["band"], "youth")

    def test_underage_loan(self):
        with self.assertRaises(IneligibleApplicant):
            check_loan_eligibility(applicant(age=17), OFFICER, AuditLog())

    def test_permission_required(self):
        with self.assertRaises(PermissionDenied):
            check_loan_eligibility(applicant(), Actor("visitor"), AuditLog())


if __name__ == "__main__":
    unittest.main()
