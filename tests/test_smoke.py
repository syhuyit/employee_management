"""Kiểm thử smoke cơ bản chạy: python -m unittest discover -s tests -v"""
import unittest

from models.department import Department
from models.employee import Employee
from models.factory import employee_from_dict
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from services.department_service import DepartmentService
from services.employee_manager import EmployeeManager
from ui.menu import MENU
from utils.exceptions import DuplicateIdError, NotFoundError


class TestSmoke(unittest.TestCase):

    def test_employee_is_abstract(self):
        """Employee() không khởi tạo trực tiếp được (lớp trừu tượng)."""
        with self.assertRaises(TypeError):
            Employee("NV001", "Nguyễn Văn An", 1990, "PB01")

    def test_fulltime_salary(self):
        """Lương FT = lương cơ bản + phụ cấp."""
        emp = FullTimeEmployee("NV001", "Nguyễn Văn An", 1990, "PB01", 10_000_000, 2_000_000)
        self.assertEqual(emp.calculate_salary(), 12_000_000)

    def test_parttime_salary(self):
        """Lương PT = số giờ làm * đơn giá giờ."""
        emp = PartTimeEmployee("NV002", "Trần Thị Bình", 1995, "PB01", 0, 100, 50_000)
        self.assertEqual(emp.calculate_salary(), 5_000_000)

    def test_polymorphism(self):
        """Đa hình: gọi calculate_salary() cho cả FT và PT đều trả về số."""
        employees = [
            FullTimeEmployee("NV001", "Nguyễn Văn An", 1990, "PB01", 10_000_000, 2_000_000),
            PartTimeEmployee("NV002", "Trần Thị Bình", 1995, "PB01", 0, 100, 50_000),
        ]
        for emp in employees:
            self.assertIsInstance(emp.calculate_salary(), (int, float))

    def test_id_normalization(self):
        """Mã nv001 được chuẩn hóa thành NV001."""
        emp = FullTimeEmployee("nv001", "Nguyễn Văn An", 1990, "PB01", 0, 0)
        self.assertEqual(emp.employee_id, "NV001")

    def test_roundtrip_fulltime(self):
        """employee_from_dict(emp.to_dict()) cho ra FullTimeEmployee cùng lương."""
        emp = FullTimeEmployee("NV001", "Nguyễn Văn An", 1990, "PB01", 10_000_000, 2_000_000)
        restored = employee_from_dict(emp.to_dict())
        self.assertIsInstance(restored, FullTimeEmployee)
        self.assertEqual(restored.calculate_salary(), emp.calculate_salary())

    def test_roundtrip_parttime(self):
        """employee_from_dict(emp.to_dict()) cho ra PartTimeEmployee cùng lương."""
        emp = PartTimeEmployee("NV002", "Trần Thị Bình", 1995, "PB01", 0, 100, 50_000)
        restored = employee_from_dict(emp.to_dict())
        self.assertIsInstance(restored, PartTimeEmployee)
        self.assertEqual(restored.calculate_salary(), emp.calculate_salary())

    def test_duplicate_employee(self):
        """Thêm cùng mã hai lần -> DuplicateIdError."""
        manager = EmployeeManager(DepartmentService())
        emp = FullTimeEmployee("NV001", "Nguyễn Văn An", 1990, "PB01", 10_000_000, 0)
        manager.add_employee(emp)
        with self.assertRaises(DuplicateIdError):
            manager.add_employee(emp)

    def test_find_not_found(self):
        """find_employee('NV999') -> NotFoundError."""
        manager = EmployeeManager(DepartmentService())
        with self.assertRaises(NotFoundError):
            manager.find_employee("NV999")

    def test_menu_handlers_callable(self):
        """Mọi giá trị trong MENU đều có handler là hàm gọi được."""
        for key, (label, handler) in MENU.items():
            self.assertTrue(callable(handler), f"Handler của '{label}' không callable.")

    def test_department_roundtrip(self):
        """Department.to_dict() / from_dict() khứ hồi đúng."""
        dept = Department("PB01", "Kỹ thuật")
        restored = Department.from_dict(dept.to_dict())
        self.assertEqual(restored.department_id, dept.department_id)
        self.assertEqual(restored.department_name, dept.department_name)


if __name__ == "__main__":
    unittest.main()
