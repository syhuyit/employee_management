"""Kiểm thử nghiệp vụ phòng ban và luồng chuyển nhân viên (Gói B)."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from models.department import Department
from models.fulltime import FullTimeEmployee
from services.department_service import DepartmentService
from ui.context import build_context
from ui.handlers.department_handler import handle_manage_departments, handle_transfer
from utils.exceptions import (
    BusinessRuleError,
    DuplicateIdError,
    NotFoundError,
    ValidationError,
)


def make_employee(employee_id: str = "NV001", department_id: str = "PB01"):
    """Tạo nhân viên toàn thời gian hợp lệ cho test."""
    return FullTimeEmployee(
        employee_id=employee_id,
        full_name="Nguyễn Văn An",
        birth_year=1990,
        department_id=department_id,
        base_salary=10_000_000,
        allowance=1_000_000,
    )


class TestDepartmentService(unittest.TestCase):
    def setUp(self) -> None:
        self.service = DepartmentService()
        self.pb01 = Department("PB01", "Kỹ thuật")
        self.pb02 = Department("PB02", "Nhân sự")
        self.service.add_department(self.pb01)
        self.service.add_department(self.pb02)

    def test_add_department_success(self):
        department = Department("PB03", "Kinh doanh")
        self.service.add_department(department)
        self.assertIs(self.service.get_department("PB03"), department)

    def test_add_department_duplicate_raises_error(self):
        with self.assertRaises(DuplicateIdError):
            self.service.add_department(Department("pb01", "Phòng khác"))

    def test_get_department_normalizes_id(self):
        self.assertIs(self.service.get_department(" pb01 "), self.pb01)

    def test_get_department_missing_raises_error(self):
        with self.assertRaises(NotFoundError):
            self.service.get_department("PB99")

    def test_update_department_success(self):
        updated = self.service.update_department("pb01", "  Kỹ   thuật mới ")
        self.assertIs(updated, self.pb01)
        self.assertEqual(updated.department_name, "Kỹ thuật mới")

    def test_update_department_invalid_name_keeps_old_name(self):
        with self.assertRaises(ValidationError):
            self.service.update_department("PB01", " ")
        self.assertEqual(self.pb01.department_name, "Kỹ thuật")

    def test_update_department_missing_raises_error(self):
        with self.assertRaises(NotFoundError):
            self.service.update_department("PB99", "Tên mới")

    def test_delete_empty_department_success(self):
        deleted = self.service.delete_department("PB02", [])
        self.assertIs(deleted, self.pb02)
        self.assertFalse(self.service.exists("PB02"))

    def test_delete_department_missing_raises_error(self):
        with self.assertRaises(NotFoundError):
            self.service.delete_department("PB99", [])

    def test_delete_department_with_one_employee_reports_count(self):
        employees = [make_employee("NV001", "PB01")]
        with self.assertRaisesRegex(
            BusinessRuleError, r"Phòng ban PB01 còn 1 nhân viên, không thể xóa\."
        ):
            self.service.delete_department("PB01", employees)
        self.assertTrue(self.service.exists("PB01"))

    def test_delete_department_with_multiple_employees_reports_count(self):
        employees = [
            make_employee("NV001", "PB01"),
            make_employee("NV002", "PB01"),
            make_employee("NV003", "PB02"),
        ]
        with self.assertRaisesRegex(
            BusinessRuleError, r"Phòng ban PB01 còn 2 nhân viên, không thể xóa\."
        ):
            self.service.delete_department("PB01", employees)
        self.assertTrue(self.service.exists("PB01"))

    def test_transfer_employee_success(self):
        employee = make_employee()
        self.service.transfer_employee(employee, "pb02")
        self.assertEqual(employee.department_id, "PB02")

    def test_transfer_to_missing_department_keeps_source(self):
        employee = make_employee()
        with self.assertRaises(NotFoundError):
            self.service.transfer_employee(employee, "PB99")
        self.assertEqual(employee.department_id, "PB01")

    def test_transfer_to_current_department_keeps_source(self):
        employee = make_employee()
        with self.assertRaises(BusinessRuleError):
            self.service.transfer_employee(employee, "pb01")
        self.assertEqual(employee.department_id, "PB01")


class TestDepartmentHandlers(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = build_context()
        self.ctx.department_service.add_department(Department("PB01", "Kỹ thuật"))
        self.ctx.department_service.add_department(Department("PB02", "Nhân sự"))
        self.employee = make_employee()
        self.ctx.employee_manager.add_employee(self.employee)

    def test_manage_menu_has_requested_order(self):
        output = io.StringIO()
        with patch(
            "ui.handlers.department_handler.input_choice", return_value="0"
        ), redirect_stdout(output):
            handle_manage_departments(self.ctx)
        text = output.getvalue()
        positions = [
            text.index("1. Thêm phòng ban"),
            text.index("2. Sửa tên phòng ban"),
            text.index("3. Xóa phòng ban"),
            text.index("4. Danh sách phòng ban"),
            text.index("0. Quay lại"),
        ]
        self.assertEqual(positions, sorted(positions))

    def test_manage_menu_reprompts_invalid_choice(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["9", "0"]), redirect_stdout(output):
            handle_manage_departments(self.ctx)
        self.assertIn("Lựa chọn không hợp lệ", output.getvalue())
        self.assertEqual(output.getvalue().count("QUẢN LÝ PHÒNG BAN"), 1)

    def test_add_handler_reprompts_invalid_and_duplicate_values(self):
        output = io.StringIO()
        with (
            patch(
                "ui.handlers.department_handler.input_choice",
                side_effect=["1", "0"],
            ),
            patch(
                "ui.handlers.department_handler.input_string",
                side_effect=["PB01", "PB03", "X", "Phòng mới"],
            ),
            redirect_stdout(output),
        ):
            handle_manage_departments(self.ctx)
        self.assertEqual(
            self.ctx.department_service.get_department("PB03").department_name,
            "Phòng mới",
        )
        self.assertIn("đã tồn tại", output.getvalue())
        self.assertIn("Vui lòng nhập lại", output.getvalue())

    def test_update_handler_reprompts_invalid_and_missing_values(self):
        output = io.StringIO()
        with (
            patch(
                "ui.handlers.department_handler.input_choice",
                side_effect=["2", "0"],
            ),
            patch(
                "ui.handlers.department_handler.input_string",
                side_effect=["AB", "PB99", "PB01", "X", "Kỹ thuật mới"],
            ),
            redirect_stdout(output),
        ):
            handle_manage_departments(self.ctx)
        self.assertEqual(
            self.ctx.department_service.get_department("PB01").department_name,
            "Kỹ thuật mới",
        )
        self.assertIn("không tìm thấy", output.getvalue().lower())
        self.assertIn("Vui lòng nhập lại", output.getvalue())

    def test_transfer_decline_does_not_change_department(self):
        output = io.StringIO()
        with (
            patch(
                "ui.handlers.department_handler.input_string",
                side_effect=["NV001", "PB02"],
            ),
            patch("ui.handlers.department_handler.confirm", return_value=False),
            redirect_stdout(output),
        ):
            handle_transfer(self.ctx)
        self.assertEqual(self.employee.department_id, "PB01")
        self.assertIn("Phòng ban hiện tại: PB01 - Kỹ thuật", output.getvalue())
        self.assertIn("Đã hủy", output.getvalue())

    def test_transfer_confirmation_reports_source_and_destination(self):
        output = io.StringIO()
        with (
            patch(
                "ui.handlers.department_handler.input_string",
                side_effect=["NV001", "PB02"],
            ),
            patch("ui.handlers.department_handler.confirm", return_value=True),
            redirect_stdout(output),
        ):
            handle_transfer(self.ctx)
        self.assertEqual(self.employee.department_id, "PB02")
        self.assertIn("Đã chuyển NV001 từ PB01 sang PB02.", output.getvalue())

    def test_transfer_reprompts_missing_or_current_destination(self):
        output = io.StringIO()
        with (
            patch(
                "ui.handlers.department_handler.input_string",
                side_effect=["NV001", "PB99", "PB01", "PB02"],
            ),
            patch("ui.handlers.department_handler.confirm", return_value=True),
            redirect_stdout(output),
        ):
            handle_transfer(self.ctx)
        self.assertEqual(self.employee.department_id, "PB02")
        self.assertIn("không tìm thấy", output.getvalue().lower())
        self.assertIn("đã thuộc phòng ban PB01", output.getvalue())


if __name__ == "__main__":
    unittest.main()
