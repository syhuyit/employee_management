"""Các hàm tìm kiếm. Nhận danh sách qua tham số, không phụ thuộc EmployeeManager."""
from models.employee import Employee


class SearchService:
    @staticmethod
    def find_by_id(employees: list[Employee], employee_id: str) -> Employee | None:
        """Tìm CHÍNH XÁC theo mã (không phân biệt hoa/thường). Không thấy -> None."""
        raise NotImplementedError("TODO(Gói D): find_by_id")

    @staticmethod
    def search_by_name(employees: list[Employee], keyword: str) -> list[Employee]:
        """Tìm GẦN ĐÚNG theo họ tên (chứa từ khóa, không phân biệt hoa/thường)."""
        raise NotImplementedError("TODO(Gói D): search_by_name")

    @staticmethod
    def search_by_department(employees: list[Employee], department_id: str) -> list[Employee]:
        """Lọc nhân viên thuộc một phòng ban (theo mã)."""
        raise NotImplementedError("TODO(Gói D): search_by_department")
