import unittest

from billing.invoices import invoice_reference
from crm.lookup import CustomerDirectory
from reports.customer_report import build_report


class ReportUsesCanonicalIds(unittest.TestCase):
    def test_report_ids_are_canonical(self):
        rows = [
            {"customer_id": "  ab 12 ", "name": "Akello Stores", "balance_minor": 1500},
            {"customer_id": "kla-0042", "name": "Mbabazi Traders", "balance_minor": 0},
        ]
        self.assertEqual(build_report(rows), ["AB-12\tAkello Stores\t1500", "KLA-0042\tMbabazi Traders\t0"])

    def test_existing_callers_still_work(self):
        self.assertEqual(invoice_reference(" kla 7", 3), "INV-KLA-7-00003")
        directory = CustomerDirectory()
        directory.add("ab 12", "Akello Stores")
        self.assertEqual(directory.find("  AB   12 "), "Akello Stores")


if __name__ == "__main__":
    unittest.main()
