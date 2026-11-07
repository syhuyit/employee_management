"""Lớp quản lý nhân viên (tách khỏi lớp thực thể)."""
from models.employee import Employee
from services.department_service import DepartmentService
from services.report_service import ReportService
from services.search_service import SearchService
from services.sort_service import SortService
from utils.exceptions import DuplicateIdError, NotFoundError
from utils.validators import validate_employee_id


class EmployeeManager:
    """Quản lý danh sách nhân viên: thêm, sửa, xóa, tra cứu."""

    def __init__(self, department_service: DepartmentService) -> None:
        self._department_service = department_service
        self._employees: dict[str, Employee] = {}

    # ===== [BASE-MIN] Gói C hoàn thiện (giữ nguyên chữ ký) =====
    def add_employee(self, employee: Employee) -> None:
        """Thêm nhân viên. Trùng mã -> DuplicateIdError (R7).
        TODO(Gói C): kiểm tra phòng ban tồn tại -> NotFoundError (R8)."""
        if employee.employee_id in self._employees:
            raise DuplicateIdError(f"Mã nhân viên {employee.employee_id} đã tồn tại.")
        self._employees[employee.employee_id] = employee

    def find_employee(self, employee_id: str) -> Employee:
        """Lấy nhân viên theo mã. Không có -> NotFoundError (R13)."""
        key = validate_employee_id(employee_id)
        if key not in self._employees:
            raise NotFoundError(f"Không tìm thấy nhân viên {key}.")
        return self._employees[key]

    def get_all(self) -> list[Employee]:
        """Trả về bản sao danh sách nhân viên."""
        return list(self._employees.values())

    def set_all(self, employees: list[Employee]) -> None:
        """Thay toàn bộ danh sách (dùng khi load file)."""
        self._employees = {e.employee_id: e for e in employees}

    def count(self) -> int:
        return len(self._employees)

    # ===== [STUB] Gói C =====
    def update_employee(self, employee_id: str, **fields) -> Employee:
        """Cập nhật các trường cho phép: full_name, birth_year, department_id, base_salary,
        allowance (FT), hours_worked, hourly_rate (PT). Không đổi mã/loại (R14).
        Phải 'tất cả hoặc không gì': một trường lỗi thì không thay đổi trường nào."""
        raise NotImplementedError("TODO(Gói C): update_employee")

    def delete_employee(self, employee_id: str) -> Employee:
        """Xóa nhân viên theo mã, trả về đối tượng đã xóa."""
        raise NotImplementedError("TODO(Gói C): delete_employee")

    # ===== KHỐI ỦY QUYỀN – KHÔNG SỬA =====
    def search_by_name(self, keyword: str) -> list[Employee]:
        return SearchService.search_by_name(self.get_all(), keyword)

    def search_by_department(self, department_id: str) -> list[Employee]:
        return SearchService.search_by_department(self.get_all(), department_id)

    def sort_employees(self, criteria: str, descending: bool = False) -> list[Employee]:
        return SortService.sort_employees(self.get_all(), criteria, descending)

    def total_salary_fund(self) -> float:
        return ReportService.total_salary_fund(self.get_all())
