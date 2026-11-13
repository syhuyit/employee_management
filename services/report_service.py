
"""Các hàm thống kê, báo cáo."""

import math

from models.employee import Employee


class ReportService:

    @staticmethod
    def total_salary_fund(employees: list[Employee]) -> float:
        """Tổng quỹ lương. Danh sách rỗng trả về 0.0."""
        return float(sum(e.calculate_salary() for e in employees))

    @staticmethod
    def count_by_department(employees: list[Employee]) -> dict[str, int]:
        """Đếm số nhân viên theo mã phòng ban."""
        result: dict[str, int] = {}

        for employee in employees:
            dept_id = employee.department_id
            result[dept_id] = result.get(dept_id, 0) + 1

        return result

    @staticmethod
    def highest_paid(employees: list[Employee]) -> list[Employee]:
        """Trả về tất cả nhân viên có mức lương cao nhất."""
        if not employees:
            return []

        salaries = [
            (employee, employee.calculate_salary())
            for employee in employees
        ]

        highest_salary = max(salary for _, salary in salaries)

        return [
            employee
            for employee, salary in salaries
            if math.isclose(salary, highest_salary, abs_tol=1e-9)
        ]

    @staticmethod
    def average_salary(employees: list[Employee]) -> float:
        """Tính lương trung bình. Danh sách rỗng trả về 0.0."""
        if not employees:
            return 0.0

        total = sum(employee.calculate_salary() for employee in employees)

        return float(total / len(employees))

    @staticmethod
    def count_by_type(employees: list[Employee]) -> dict[str, int]:
        """Đếm số lượng nhân viên theo loại."""
        result: dict[str, int] = {}

        for employee in employees:
            employee_type = type(employee).__name__.removesuffix("Employee")
            result[employee_type] = result.get(employee_type, 0) + 1

        return result
