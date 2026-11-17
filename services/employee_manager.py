"""Lớp quản lý nhân viên (tách khỏi lớp thực thể)."""
from models.employee import Employee
from services.department_service import DepartmentService
from services.report_service import ReportService
from services.search_service import SearchService
from services.sort_service import SortService
from utils.exceptions import DuplicateIdError, NotFoundError, ValidationError
from utils.validators import validate_employee_id


class EmployeeManager:
    """Quản lý danh sách nhân viên: thêm, sửa, xóa, tra cứu."""

    def __init__(self, department_service: DepartmentService) -> None:
        self._department_service = department_service
        self._employees: dict[str, Employee] = {}

    # ===== [BASE-MIN] Gói C hoàn thiện (giữ nguyên chữ ký) =====
    def add_employee(self, employee: Employee) -> None:
        """Thêm nhân viên. Trùng mã -> DuplicateIdError (R7).
        Kiểm tra phòng ban tồn tại -> NotFoundError (R8)."""
        if employee.employee_id in self._employees:
            raise DuplicateIdError(f"Mã nhân viên {employee.employee_id} đã tồn tại.")
        # Danh sách phòng ban rỗng không có nghĩa là mã phòng ban bất kỳ đều hợp lệ.
        if not self._department_service.exists(employee.department_id):
            raise NotFoundError(f"Phòng ban {employee.department_id} không tồn tại.")
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
        emp = self.find_employee(employee_id)

        if not fields:
            return emp

        # Xác định trường cho phép theo loại nhân viên
        allowed_fields = {"full_name", "birth_year", "department_id", "base_salary"}
        if emp.employee_type == "FullTime":
            allowed_fields.add("allowance")
        elif emp.employee_type == "PartTime":
            allowed_fields.update({"hours_worked", "hourly_rate"})

        # Kiểm tra trường không được phép
        for field in fields:
            if field not in allowed_fields:
                raise ValidationError(
                    f"Trường '{field}' không được phép cập nhật cho nhân viên {emp.employee_type} (R14)."
                )

        # Kiểm tra phòng ban mới tồn tại nếu cập nhật department_id
        if "department_id" in fields:
            new_dept_id = str(fields["department_id"]).strip().upper()
            if not self._department_service.exists(new_dept_id):
                raise NotFoundError(f"Phòng ban {new_dept_id} không tồn tại (R8).")

        # Cơ chế 'Tất cả hoặc không gì': Lưu giá trị cũ trước khi gán
        backup = {field: getattr(emp, field) for field in fields}
        applied = []
        try:
            for field, value in fields.items():
                setattr(emp, field, value)
                applied.append(field)
        except Exception:
            # Khôi phục lại toàn bộ trường đã thay đổi nếu gặp lỗi
            for field in applied:
                setattr(emp, field, backup[field])
            raise

        return emp

    def delete_employee(self, employee_id: str) -> Employee:
        """Xóa nhân viên theo mã, trả về đối tượng đã xóa. Không tồn tại -> NotFoundError (R13)."""
        emp = self.find_employee(employee_id)
        del self._employees[emp.employee_id]
        return emp

    # ===== KHỐI ỦY QUYỀN – KHÔNG SỬA =====
    def search_by_name(self, keyword: str) -> list[Employee]:
        return SearchService.search_by_name(self.get_all(), keyword)

    def search_by_department(self, department_id: str) -> list[Employee]:
        return SearchService.search_by_department(self.get_all(), department_id)

    def sort_employees(self, criteria: str, descending: bool = False) -> list[Employee]:
        return SortService.sort_employees(self.get_all(), criteria, descending)

    def total_salary_fund(self) -> float:
        return ReportService.total_salary_fund(self.get_all())
