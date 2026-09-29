"""Exceptions that form part of the public eligibility contract."""


class PermissionDenied(Exception):
    """The acting user may not evaluate this applicant."""


class IneligibleApplicant(Exception):
    """The applicant does not meet a policy rule."""


class InvalidApplicant(ValueError):
    """The applicant record is malformed."""
