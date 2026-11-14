
"""Các hàm sắp xếp."""
import unicodedata

from models.employee import Employee
from utils.exceptions import ValidationError


SORT_CRITERIA = ("salary", "name", "id", "birth_year")


class SortService:
    @staticmethod
    def sort_employees(
        employees: list[Employee],
        criteria: str,
        descending: bool = False
    ) -> list[Employee]:
        """Trả về danh sách MỚI đã sắp xếp (không sửa danh sách gốc).
        criteria thuộc SORT_CRITERIA, sai -> ValidationError.
        """

        # Kiểm tra tiêu chí sắp xếp
        if criteria not in SORT_CRITERIA:
            raise ValidationError(
                f"Tiêu chí sắp xếp không hợp lệ: {criteria}"
            )

        # Tạo bản sao danh sách để không làm thay đổi danh sách gốc
        employees_copy = list(employees)

        # Chuẩn hóa chuỗi tiếng Việt để sắp xếp
        def normalize_text(text: str) -> str:
            text = text.casefold().replace("đ", "d")
            text = unicodedata.normalize("NFD", text)

            # Loại bỏ dấu tiếng Việt
            text = "".join(
                char for char in text
                if unicodedata.category(char) != "Mn"
            )

            return text

        # Xây dựng khóa sắp xếp theo tiêu chí
        if criteria == "salary":
            key_function = lambda emp: emp.calculate_salary()

        elif criteria == "name":
            def key_function(emp):
                full_name = normalize_text(emp.full_name.strip())
                name_parts = full_name.split()

                # Lấy từ cuối cùng của họ tên để sắp xếp trước
                last_name = name_parts[-1] if name_parts else ""

                # Sau đó xét toàn bộ họ tên
                return last_name, full_name

        elif criteria == "id":
            key_function = lambda emp: emp.employee_id.casefold()

        else:  # birth_year
            key_function = lambda emp: emp.birth_year

        # sorted() tạo danh sách mới và giữ thứ tự ban đầu
        # khi hai phần tử có cùng khóa sắp xếp (stable sort)
        return sorted(
            employees_copy,
            key=key_function,
            reverse=descending
        )
