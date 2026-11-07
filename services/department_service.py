"""Quản lý phòng ban và nghiệp vụ chuyển phòng ban."""
from models.department import Department
from models.employee import Employee
from utils.exceptions import DuplicateIdError, NotFoundError
from utils.validators import validate_department_id


class DepartmentService:
    """Lớp quản lý danh sách phòng ban."""

    def __init__(self) -> None:
        self._departments: dict[str, Department] = {}

    # ----- [BASE-MIN] -----
    def add_department(self, department: Department) -> None:
        """Thêm phòng ban. Trùng mã -> DuplicateIdError (R9)."""
        if department.department_id in self._departments:
            raise DuplicateIdError(f"Mã phòng ban {department.department_id} đã tồn tại.")
        self._departments[department.department_id] = department

    def get_department(self, department_id: str) -> Department:
        """Lấy phòng ban theo mã. Không có -> NotFoundError."""
        key = validate_department_id(department_id)
        if key not in self._departments:
            raise NotFoundError(f"Không tìm thấy phòng ban {key}.")
        return self._departments[key]

    def exists(self, department_id: str) -> bool:
        """Kiểm tra phòng ban có tồn tại không (không ném lỗi)."""
        return str(department_id).strip().upper() in self._departments

    def get_all(self) -> list[Department]:
        return list(self._departments.values())

    def set_all(self, departments: list[Department]) -> None:
        """Thay toàn bộ danh sách (dùng khi load file)."""
        self._departments = {d.department_id: d for d in departments}

    # ----- [STUB] -----
    def update_department(self, department_id: str, new_name: str) -> Department:
        """Đổi tên phòng ban. Trả về phòng ban đã cập nhật."""
        raise NotImplementedError("TODO(Gói B): update_department")

    def delete_department(self, department_id: str, employees: list[Employee]) -> Department:
        """Xóa phòng ban. Còn nhân viên -> BusinessRuleError (R10). Trả về phòng ban đã xóa."""
        raise NotImplementedError("TODO(Gói B): delete_department")

    def transfer_employee(self, employee: Employee, new_department_id: str) -> None:
        """Chuyển nhân viên sang phòng ban mới (R11, R12)."""
        raise NotImplementedError("TODO(Gói B): transfer_employee")
