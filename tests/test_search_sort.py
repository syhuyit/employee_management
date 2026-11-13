
"""Kiểm thử chức năng tìm kiếm và sắp xếp nhân viên (Gói D)."""

import unittest

from models.employee import Employee
from services.search_service import SearchService
from services.sort_service import SortService
from utils.exceptions import ValidationError


class FakeEmployee:
    """Đối tượng nhân viên giả phục vụ kiểm thử."""

    def __init__(
        self,
        employee_id,
        full_name,
        birth_year,
        department_id,
        base_salary,
        salary=None,
    ):
        self.employee_id = employee_id
        self.full_name = full_name
        self.birth_year = birth_year
        self.department_id = department_id
        self.base_salary = base_salary
        self._salary = salary if salary is not None else base_salary

    def calculate_salary(self):
        return self._salary


class TestSearchService(unittest.TestCase):
    """Kiểm thử các chức năng tìm kiếm."""

    def setUp(self):
        self.employees = [
            FakeEmployee("NV01", "Nguyen Van An", 2002, "PB01", 10000000),
            FakeEmployee("NV02", "Tran Thi Binh", 2001, "PB02", 12000000),
            FakeEmployee("NV03", "Le Van Cuong", 2003, "PB01", 9000000),
            FakeEmployee("NV04", "Pham Thi Dung", 2000, "PB03", 15000000),
        ]

    def test_find_by_id_success(self):
        """Tìm nhân viên theo mã chính xác."""
        result = SearchService.find_by_id(self.employees, "NV01")
        self.assertIsNotNone(result)
        self.assertEqual(result.employee_id, "NV01")

    def test_find_by_id_case_insensitive(self):
        """Tìm mã nhân viên không phân biệt chữ hoa, chữ thường."""
        result = SearchService.find_by_id(self.employees, "nv01")
        self.assertIsNotNone(result)
        self.assertEqual(result.employee_id, "NV01")

    def test_find_by_id_not_found(self):
        """Không tìm thấy mã nhân viên thì trả về None."""
        result = SearchService.find_by_id(self.employees, "NV99")
        self.assertIsNone(result)

    def test_search_by_name_partial(self):
        """Tìm kiếm họ tên bằng một phần từ khóa."""
        result = SearchService.search_by_name(self.employees, "Van")
        self.assertEqual(len(result), 2)

    def test_search_by_name_case_insensitive(self):
        """Tìm kiếm họ tên không phân biệt hoa, thường."""
        result = SearchService.search_by_name(self.employees, "NGUYEN")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].employee_id, "NV01")

    def test_search_by_name_empty_keyword(self):
        """Từ khóa rỗng trả về danh sách rỗng."""
        result = SearchService.search_by_name(self.employees, "")
        self.assertEqual(result, [])

    def test_search_by_name_accent_insensitive(self):
        """Tìm kiếm họ tên không phân biệt dấu tiếng Việt."""
        employees = [
            FakeEmployee("NV05", "Nguyễn Văn Ánh", 2002, "PB01", 10000000)
        ]
        result = SearchService.search_by_name(employees, "nguyen van anh")
        self.assertEqual(len(result), 1)

    def test_search_by_department_success(self):
        """Lọc nhân viên theo mã phòng ban."""
        result = SearchService.search_by_department(
            self.employees, "PB01"
        )
        self.assertEqual(len(result), 2)
        self.assertTrue(
            all(employee.department_id == "PB01" for employee in result)
        )

    def test_search_by_department_case_insensitive(self):
        """Mã phòng ban không phân biệt hoa, thường."""
        result = SearchService.search_by_department(
            self.employees, "pb01"
        )
        self.assertEqual(len(result), 2)

    def test_search_by_department_not_found(self):
        """Phòng ban không tồn tại trả về danh sách rỗng."""
        result = SearchService.search_by_department(
            self.employees, "PB99"
        )
        self.assertEqual(result, [])


class TestSortService(unittest.TestCase):
    """Kiểm thử các chức năng sắp xếp."""

    def setUp(self):
        self.employees = [
            FakeEmployee("NV03", "Le Van Cuong", 2003, "PB01", 9000000),
            FakeEmployee("NV01", "Nguyen Van An", 2002, "PB01", 10000000),
            FakeEmployee("NV04", "Pham Thi Dung", 2000, "PB03", 15000000),
            FakeEmployee("NV02", "Tran Thi Binh", 2001, "PB02", 12000000),
        ]

    def test_sort_by_salary_ascending(self):
        """Sắp xếp lương tăng dần."""
        result = SortService.sort_employees(
            self.employees, "salary", False
        )
        salaries = [employee.base_salary for employee in result]
        self.assertEqual(salaries, sorted(salaries))

    def test_sort_by_salary_descending(self):
        """Sắp xếp lương giảm dần."""
        result = SortService.sort_employees(
            self.employees, "salary", True
        )
        salaries = [employee.base_salary for employee in result]
        self.assertEqual(salaries, sorted(salaries, reverse=True))

    def test_sort_by_name(self):
        """Sắp xếp theo họ tên."""
        result = SortService.sort_employees(
            self.employees, "name", False
        )
        self.assertEqual(
            [employee.employee_id for employee in result],
            ["NV01", "NV02", "NV03", "NV04"],
        )

    def test_sort_by_id(self):
        """Sắp xếp theo mã nhân viên."""
        result = SortService.sort_employees(
            self.employees, "id", False
        )
        self.assertEqual(
            [employee.employee_id for employee in result],
            ["NV01", "NV02", "NV03", "NV04"],
        )

    def test_sort_by_birth_year(self):
        """Sắp xếp theo năm sinh tăng dần."""
        result = SortService.sort_employees(
            self.employees, "birth_year", False
        )
        years = [employee.birth_year for employee in result]
        self.assertEqual(years, sorted(years))

    def test_sort_does_not_modify_original_list(self):
        """Sắp xếp không làm thay đổi danh sách ban đầu."""
        original = self.employees.copy()

        SortService.sort_employees(self.employees, "salary", True)

        self.assertEqual(self.employees, original)

    def test_sort_returns_new_list(self):
        """Kết quả sắp xếp là một danh sách mới."""
        result = SortService.sort_employees(
            self.employees, "salary", False
        )
        self.assertIsNot(result, self.employees)

    def test_sort_invalid_criteria(self):
        """Tiêu chí không hợp lệ phải phát sinh ValidationError."""
        with self.assertRaises(ValidationError):
            SortService.sort_employees(
                self.employees, "invalid", False
            )


if __name__ == "__main__":
    unittest.main()
