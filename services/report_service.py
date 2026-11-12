"""Các hàm thống kê, báo cáo."""
from models.employee import Employee

class ReportService:
    @staticmethod
    def total_salary_fund(employees: list[Employee]) -> float:
        """Tổng quỹ lương (tổng calculate_salary). Danh sách rỗng -> 0.0."""
        raise NotImplementedError("TODO(Gói E): total_salary_fund")

    @staticmethod
    def count_by_department(employees: list[Employee]) -> dict[str, int]:
        """Số nhân viên theo mã phòng ban: {'PB01': 3, ...}."""
        raise NotImplementedError("TODO(Gói E): count_by_department")

    @staticmethod
    def highest_paid(employees: list[Employee]) -> list[Employee]:
        """Danh sách nhân viên lương cao nhất (có thể nhiều người nếu đồng hạng). Rỗng -> []."""
        raise NotImplementedError("TODO(Gói E): highest_paid")

    @staticmethod
    def average_salary(employees: list[Employee]) -> float:
        """Lương trung bình. Rỗng -> 0.0."""
        raise NotImplementedError("TODO(Gói E): average_salary")

    @staticmethod
    def count_by_type(employees: list[Employee]) -> dict[str, int]:
        """Số nhân viên theo loại: {'FullTime': 4, 'PartTime': 2}."""
        raise NotImplementedError("TODO(Gói E): count_by_type")
