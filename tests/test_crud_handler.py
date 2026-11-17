"""Tests for employee creation input and error flows."""

import io
import unittest
from contextlib import redirect_stdout
from datetime import date
from unittest.mock import patch

from models.department import Department
from models.fulltime import FullTimeEmployee
from ui.context import build_context
from ui.handlers.crud_handler import handle_add


class TestAddEmployeeHandler(unittest.TestCase):
    def setUp(self):
        self.ctx = build_context()
        self.ctx.department_service.add_department(Department("PB01", "Kỹ thuật"))

    def test_duplicate_employee_id_reports_error_and_returns(self):
        existing = FullTimeEmployee(
            "NV001", "Nguyễn Văn An", 1990, "PB01", 10_000_000, 1_000_000
        )
        self.ctx.employee_manager.add_employee(existing)
        output = io.StringIO()

        with (
            patch("ui.handlers.crud_handler.input_choice", return_value="1"),
            patch("builtins.input", return_value="NV001") as input_mock,
            redirect_stdout(output),
        ):
            handle_add(self.ctx)

        self.assertIn("đã tồn tại", output.getvalue())
        input_mock.assert_called_once()
        self.assertEqual(self.ctx.employee_manager.count(), 1)

    def test_missing_department_reports_error_and_returns(self):
        current_year = date.today().year
        output = io.StringIO()

        with (
            patch("ui.handlers.crud_handler.input_choice", return_value="1"),
            patch(
                "builtins.input",
                side_effect=["NV002", "Trần Thị Bình", str(current_year - 30), "PB99"],
            ) as input_mock,
            redirect_stdout(output),
        ):
            handle_add(self.ctx)

        self.assertIn("Phòng ban 'PB99' không tồn tại", output.getvalue())
        self.assertEqual(input_mock.call_count, 4)
        self.assertEqual(self.ctx.employee_manager.count(), 0)

    def test_invalid_field_reprompts_that_field_and_adds_employee(self):
        output = io.StringIO()

        with (
            patch("ui.handlers.crud_handler.input_choice", return_value="1"),
            patch(
                "builtins.input",
                side_effect=[
                    "X",
                    "NV002",
                    "Trần Thị Bình",
                    "1990",
                    "PB01",
                    "15000000",
                    "1000000",
                ],
            ),
            redirect_stdout(output),
        ):
            handle_add(self.ctx)

        employee = self.ctx.employee_manager.find_employee("NV002")
        self.assertEqual(employee.department_id, "PB01")
        self.assertIn("Vui lòng nhập lại", output.getvalue())
        self.assertIn("Thêm nhân viên thành công", output.getvalue())


if __name__ == "__main__":
    unittest.main()
