"""Unit test cho ReportService (Goi E)."""
import unittest

from services.report_service import ReportService


class _FakeEmployee:
    """Nhan vien gia: chi can department_id va calculate_salary()."""

    def __init__(self, employee_id, department_id, salary):
        self.employee_id = employee_id
        self.department_id = department_id
        self._salary = salary

    def calculate_salary(self):
        return self._salary


class FullTimeEmployee(_FakeEmployee):
    pass


class PartTimeEmployee(_FakeEmployee):
    pass


class TestReportService(unittest.TestCase):
    def setUp(self):
        self.a = FullTimeEmployee("NV01", "PB01", 10_000_000)
        self.b = FullTimeEmployee("NV02", "PB01", 15_000_000)
        self.c = PartTimeEmployee("NV03", "PB02", 5_000_000)
        self.employees = [self.a, self.b, self.c]

    # ---- total_salary_fund ----
    def test_total_salary_fund(self):
        self.assertEqual(ReportService.total_salary_fund(self.employees), 30_000_000)

    def test_total_salary_fund_empty(self):
        result = ReportService.total_salary_fund([])
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_total_salary_fund_single(self):
        self.assertEqual(ReportService.total_salary_fund([self.a]), 10_000_000)

    # ---- count_by_department ----
    def test_count_by_department(self):
        self.assertEqual(
            ReportService.count_by_department(self.employees),
            {"PB01": 2, "PB02": 1},
        )

    def test_count_by_department_empty(self):
        self.assertEqual(ReportService.count_by_department([]), {})

    # ---- highest_paid ----
    def test_highest_paid_single_winner(self):
        self.assertEqual(ReportService.highest_paid(self.employees), [self.b])

    def test_highest_paid_tie(self):
        d = PartTimeEmployee("NV04", "PB02", 15_000_000)
        result = ReportService.highest_paid(self.employees + [d])
        self.assertEqual(len(result), 2)
        self.assertIn(self.b, result)
        self.assertIn(d, result)

    def test_highest_paid_empty(self):
        self.assertEqual(ReportService.highest_paid([]), [])

    def test_highest_paid_float_tie(self):
        # 0.1 + 0.2 != 0.3 theo so thuc, van phai tinh la dong hang
        x = FullTimeEmployee("NV05", "PB01", 0.1 + 0.2)
        y = FullTimeEmployee("NV06", "PB01", 0.3)
        self.assertEqual(len(ReportService.highest_paid([x, y])), 2)

    # ---- average_salary ----
    def test_average_salary(self):
        self.assertEqual(ReportService.average_salary(self.employees), 10_000_000)

    def test_average_salary_empty(self):
        self.assertEqual(ReportService.average_salary([]), 0.0)

    # ---- count_by_type ----
    def test_count_by_type(self):
        self.assertEqual(
            ReportService.count_by_type(self.employees),
            {"FullTime": 2, "PartTime": 1},
        )

    def test_count_by_type_empty(self):
        self.assertEqual(ReportService.count_by_type([]), {})


if __name__ == "__main__":
    unittest.main()