"""Unit tests for employee models.

Các test này kiểm tra:
- Lớp `Employee` là abstract và không thể khởi tạo.
- `FullTimeEmployee` và `PartTimeEmployee` tính lương đúng.
- Đa hình: danh sách các đối tượng khác nhau đều có thể gọi `calculate_salary`.
- Các setter báo `ValidationError` khi dữ liệu không hợp lệ.
- `to_dict` / `from_dict` / `employee_from_dict` trả về đối tượng cùng lớp và cùng lương.
- Kiểm tra các ràng buộc biên đã định nghĩa trong `validators`.
"""

from datetime import date
import unittest

from models.employee import Employee
from models.factory import employee_from_dict
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from utils.exceptions import ValidationError
from utils.validators import (
    validate_birth_year,
    validate_full_name,
    validate_hours_worked,
    validate_identifier,
)


class TestEmployeeModels(unittest.TestCase):
    def test_employee_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Employee("NV001", "Nguyen Van A", 1990, "PB01", 1000.0)

    def test_fulltime_salary_calculation(self):
        emp = FullTimeEmployee(
            "NV001", "Nguyen Van A", 1990, "PB01", 15000000, 2000000
        )

        self.assertEqual(emp.calculate_salary(), 17000000)
        self.assertIn("Phụ cấp: 2,000,000", str(emp))

    def test_parttime_salary_calculation(self):
        emp = PartTimeEmployee(
            "NV002", "Le Thi B", 1995, "PB02", 0.0,
            hours_worked=40, hourly_rate=200000,
        )

        self.assertEqual(emp.calculate_salary(), 8000000)
        self.assertIn("Giờ: 40", str(emp))
        self.assertIn("Đơn giá: 200,000", str(emp))

    def test_fulltime_dict_roundtrip(self):
        original = FullTimeEmployee(
            "NV003", "Tran Van C", 1985, "PB03", 12000000, 1500000
        )
        restored = employee_from_dict(original.to_dict())

        self.assertIsInstance(restored, FullTimeEmployee)
        self.assertEqual(restored.calculate_salary(), original.calculate_salary())

    def test_parttime_dict_roundtrip(self):
        original = PartTimeEmployee(
            "NV004", "Pham D", 1992, "PB04", 0.0, 30, 250000
        )
        restored = employee_from_dict(original.to_dict())

        self.assertIsInstance(restored, PartTimeEmployee)
        self.assertEqual(restored.calculate_salary(), original.calculate_salary())

    def test_factory_invalid_type(self):
        with self.assertRaises(ValidationError):
            employee_from_dict({"type": "Unknown", "employee_id": "NV005"})

    def test_factory_missing_field(self):
        data = {"type": "FullTime", "employee_id": "NV006"}

        with self.assertRaises(ValidationError):
            employee_from_dict(data)

    def test_setters_validation_errors(self):
        emp = FullTimeEmployee(
            "NV007", "Hoang E", 1990, "PB05", 1000000, 500000
        )
        current_year = date.today().year

        with self.assertRaises(AttributeError):
            emp.employee_id = "NV999"
        with self.assertRaises(ValidationError):
            emp.full_name = "A1"
        with self.assertRaises(ValidationError):
            emp.birth_year = current_year - 17
        with self.assertRaises(ValidationError):
            emp.department_id = "ab"
        with self.assertRaises(ValidationError):
            emp.base_salary = -1000
        with self.assertRaises(ValidationError):
            emp.allowance = -500

    def test_fulltime_zero_allowance_keeps_base_salary(self):
        emp = FullTimeEmployee("NV008", "Hoang F", 1990, "PB05", 1000000, 0)

        self.assertEqual(emp.allowance, 0)
        self.assertEqual(emp.calculate_salary(), 1000000)

    def test_parttime_zero_hours_results_in_zero_salary(self):
        emp = PartTimeEmployee("NV009", "Tran G", 1990, "PB05", 0, 0, 200000)

        self.assertEqual(emp.calculate_salary(), 0)

    def test_parttime_hours_setter_rejects_value_above_limit(self):
        emp = PartTimeEmployee("NV010", "Le H", 1990, "PB05", 0, 40, 200000)

        with self.assertRaises(ValidationError):
            emp.hours_worked = 301

    def test_identifier_boundary(self):
        self.assertEqual(validate_identifier("abc"), "ABC")
        self.assertEqual(validate_identifier("ABCDEFGHIJ"), "ABCDEFGHIJ")
        with self.assertRaises(ValidationError):
            validate_identifier("ABCDEFGHIJK")

    def test_full_name_boundary(self):
        self.assertEqual(validate_full_name("An"), "An")
        self.assertEqual(validate_full_name("  An   B "), "An B")
        with self.assertRaises(ValidationError):
            validate_full_name("A")

    def test_birth_year_boundary(self):
        current_year = date.today().year
        self.assertEqual(
            validate_birth_year(current_year - 18), current_year - 18
        )
        self.assertEqual(
            validate_birth_year(current_year - 65), current_year - 65
        )
        with self.assertRaises(ValidationError):
            validate_birth_year(current_year - 17)
        with self.assertRaises(ValidationError):
            validate_birth_year(current_year - 66)

    def test_hours_worked_boundary(self):
        self.assertEqual(validate_hours_worked(0), 0.0)
        self.assertEqual(validate_hours_worked(300), 300.0)
        with self.assertRaises(ValidationError):
            validate_hours_worked(301)


if __name__ == "__main__":
    unittest.main()
