"""Các hàm sắp xếp."""
from models.employee import Employee

SORT_CRITERIA = ("salary", "name", "id", "birth_year")


class SortService:
    @staticmethod
    def sort_employees(employees: list[Employee], criteria: str, descending: bool = False) -> list[Employee]:
        """Trả về danh sách MỚI đã sắp xếp (không sửa danh sách gốc).
        criteria thuộc SORT_CRITERIA, sai -> ValidationError."""
        raise NotImplementedError("TODO(Gói D): sort_employees")
