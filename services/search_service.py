
"""Các hàm tìm kiếm. Nhận danh sách qua tham số, không phụ thuộc EmployeeManager."""
import unicodedata
from models.employee import Employee


class SearchService:
    @staticmethod
    def find_by_id(employees: list[Employee], employee_id: str) -> Employee | None:
        """Tìm CHÍNH XÁC theo mã (không phân biệt hoa/thường). Không thấy -> None."""
        # Chuẩn hóa mã tìm kiếm
        search_id = employee_id.strip().casefold()

        # Duyệt danh sách nhân viên để tìm mã trùng khớp chính xác
        for employee in employees:
            if employee.employee_id.strip().casefold() == search_id:
                return employee

        # Không tìm thấy nhân viên
        return None

    @staticmethod
    def search_by_name(employees: list[Employee], keyword: str) -> list[Employee]:
        """Tìm GẦN ĐÚNG theo họ tên (chứa từ khóa, không phân biệt hoa/thường)."""

        # Từ khóa rỗng hoặc chỉ chứa khoảng trắng thì trả về danh sách rỗng
        if not keyword or not keyword.strip():
            return []

        # Hàm chuẩn hóa chuỗi: chuyển chữ thường và loại bỏ dấu tiếng Việt
        def normalize_text(text: str) -> str:
            text = text.casefold().replace("đ", "d")
            text = unicodedata.normalize("NFD", text)

            # Loại bỏ các ký tự dấu
            text = "".join(
                char for char in text
                if unicodedata.category(char) != "Mn"
            )

            return text

        # Chuẩn hóa từ khóa tìm kiếm
        search_keyword = normalize_text(keyword.strip())

        result = []

        # Tìm những nhân viên có họ tên chứa từ khóa
        for employee in employees:
            full_name = normalize_text(employee.full_name)

            if search_keyword in full_name:
                result.append(employee)

        return result

    @staticmethod
    def search_by_department(employees: list[Employee], department_id: str) -> list[Employee]:
        """Lọc nhân viên thuộc một phòng ban (theo mã)."""

        # Mã phòng ban rỗng thì trả về danh sách rỗng
        if not department_id or not department_id.strip():
            return []

        # Chuẩn hóa mã phòng ban
        search_department_id = department_id.strip().casefold()

        result = []

        # Lọc nhân viên theo mã phòng ban
        for employee in employees:
            if employee.department_id.strip().casefold() == search_department_id:
                result.append(employee)

        return result
