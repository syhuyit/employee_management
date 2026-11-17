"""Unit test cho EmployeeManager (Gói C)."""
import unittest

from models.department import Department
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from services.department_service import DepartmentService
from services.employee_manager import EmployeeManager
from utils.exceptions import DuplicateIdError, NotFoundError, ValidationError


class TestEmployeeManager(unittest.TestCase):
    def setUp(self):
        self.dept_service = DepartmentService()
        self.dept_service.add_department(Department("PB01", "Kỹ thuật"))
        self.dept_service.add_department(Department("PB02", "Nhân sự"))
        self.manager = EmployeeManager(self.dept_service)

        self.ft = FullTimeEmployee(
            "NV001", "Nguyễn Văn An", 1990, "PB01", 15_000_000, 2_000_000
        )
        self.pt = PartTimeEmployee(
            "NV002", "Trần Thị Bình", 1995, "PB02", 0.0, 80, 50_000
        )

    # 1. Thêm nhân viên
    def test_add_employee_success(self):
        self.manager.add_employee(self.ft)
        self.assertEqual(self.manager.count(), 1)
        found = self.manager.find_employee("NV001")
        self.assertEqual(found.full_name, "Nguyễn Văn An")

    def test_add_parttime_employee_success(self):
        self.manager.add_employee(self.pt)
        self.assertEqual(self.manager.count(), 1)
        found = self.manager.find_employee("NV002")
        self.assertEqual(found.employee_type, "PartTime")

    def test_add_duplicate_employee_id_raises_duplicate_error(self):
        self.manager.add_employee(self.ft)
        duplicate_emp = FullTimeEmployee(
            "NV001", "Lê Văn C", 1992, "PB01", 10_000_000, 1_000_000
        )
        with self.assertRaises(DuplicateIdError):
            self.manager.add_employee(duplicate_emp)

    def test_add_employee_non_existent_department_raises_not_found(self):
        emp_bad_dept = FullTimeEmployee(
            "NV003", "Hoàng Văn D", 1993, "PB99", 10_000_000, 1_000_000
        )
        with self.assertRaises(NotFoundError):
            self.manager.add_employee(emp_bad_dept)

    def test_add_employee_rejects_missing_department_when_no_departments_exist(self):
        empty_department_service = DepartmentService()
        manager = EmployeeManager(empty_department_service)
        employee = FullTimeEmployee(
            "NV003", "Hoàng Văn D", 1993, "PB99", 10_000_000, 1_000_000
        )

        with self.assertRaises(NotFoundError):
            manager.add_employee(employee)
        self.assertEqual(manager.count(), 0)

    # 2. Tìm kiếm nhân viên
    def test_find_employee_case_insensitive(self):
        self.manager.add_employee(self.ft)
        found = self.manager.find_employee("nv001")
        self.assertEqual(found.employee_id, "NV001")

    def test_find_employee_not_found_raises_not_found(self):
        with self.assertRaises(NotFoundError):
            self.manager.find_employee("NV999")

    # 3. Cập nhật nhân viên
    def test_update_employee_full_name(self):
        self.manager.add_employee(self.ft)
        updated = self.manager.update_employee("NV001", full_name="Nguyễn Văn Bình")
        self.assertEqual(updated.full_name, "Nguyễn Văn Bình")

    def test_update_employee_birth_year(self):
        self.manager.add_employee(self.ft)
        updated = self.manager.update_employee("NV001", birth_year=1992)
        self.assertEqual(updated.birth_year, 1992)

    def test_update_employee_base_salary(self):
        self.manager.add_employee(self.ft)
        updated = self.manager.update_employee("NV001", base_salary=18_000_000)
        self.assertEqual(updated.base_salary, 18_000_000)

    def test_update_fulltime_allowance(self):
        self.manager.add_employee(self.ft)
        updated = self.manager.update_employee("NV001", allowance=3_000_000)
        self.assertEqual(updated.allowance, 3_000_000)

    def test_update_parttime_hours_worked(self):
        self.manager.add_employee(self.pt)
        updated = self.manager.update_employee("NV002", hours_worked=100)
        self.assertEqual(updated.hours_worked, 100)

    def test_update_parttime_hourly_rate(self):
        self.manager.add_employee(self.pt)
        updated = self.manager.update_employee("NV002", hourly_rate=60_000)
        self.assertEqual(updated.hourly_rate, 60_000)
        self.assertEqual(updated.calculate_salary(), 4_800_000)

    def test_update_employee_department_success(self):
        self.manager.add_employee(self.ft)
        updated = self.manager.update_employee("NV001", department_id="PB02")
        self.assertEqual(updated.department_id, "PB02")

    def test_update_employee_department_not_found(self):
        self.manager.add_employee(self.ft)
        with self.assertRaises(NotFoundError):
            self.manager.update_employee("NV001", department_id="PB99")

    def test_update_forbidden_fields_raises_validation_error(self):
        self.manager.add_employee(self.ft)
        # Không được đổi type
        with self.assertRaises(ValidationError):
            self.manager.update_employee("NV001", type="PartTime")
        # Không được đổi trường không hợp lệ
        with self.assertRaises(ValidationError):
            self.manager.update_employee("NV001", role="Manager")

    def test_update_mismatched_type_field_raises_validation_error(self):
        self.manager.add_employee(self.pt)
        # PartTime không có allowance
        with self.assertRaises(ValidationError):
            self.manager.update_employee("NV002", allowance=1_000_000)

        self.manager.add_employee(self.ft)
        # FullTime không có hours_worked
        with self.assertRaises(ValidationError):
            self.manager.update_employee("NV001", hours_worked=50)

    def test_update_all_or_nothing_rollback_on_error(self):
        self.manager.add_employee(self.ft)
        old_name = self.ft.full_name
        old_salary = self.ft.base_salary

        # Cố gắng đổi full_name (hợp lệ) và base_salary = -5000 (âm, không hợp lệ)
        with self.assertRaises(ValidationError):
            self.manager.update_employee(
                "NV001", full_name="Tên Mới", base_salary=-5000
            )

        # Kiểm tra: cả full_name lẫn base_salary đều không bị đổi
        checked = self.manager.find_employee("NV001")
        self.assertEqual(checked.full_name, old_name)
        self.assertEqual(checked.base_salary, old_salary)

    # 4. Xóa nhân viên
    def test_delete_employee_success(self):
        self.manager.add_employee(self.ft)
        deleted = self.manager.delete_employee("NV001")
        self.assertEqual(deleted.employee_id, "NV001")
        self.assertEqual(self.manager.count(), 0)
        with self.assertRaises(NotFoundError):
            self.manager.find_employee("NV001")

    def test_delete_employee_not_found(self):
        with self.assertRaises(NotFoundError):
            self.manager.delete_employee("NV999")

    # 5. get_all và set_all
    def test_get_all_returns_copy_of_list(self):
        self.manager.add_employee(self.ft)
        emps = self.manager.get_all()
        self.assertEqual(len(emps), 1)
        emps.clear()
        self.assertEqual(self.manager.count(), 1)

    def test_set_all_replaces_all_employees(self):
        self.manager.add_employee(self.ft)
        self.assertEqual(self.manager.count(), 1)
        self.manager.set_all([self.pt])
        self.assertEqual(self.manager.count(), 1)
        self.assertEqual(self.manager.get_all()[0].employee_id, "NV002")


if __name__ == "__main__":
    unittest.main()
