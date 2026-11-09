"""Lớp trừu tượng Employee  lớp cha của mọi loại nhân viên.

- Thuộc tính được lưu ở dạng private (được tiền tố `__`).
- Truy cập thông qua `@property`/setter để thực hiện kiểm tra dữ liệu.
- `employee_id` chỉ cung cấp getter → thuộc tính chỉ đọc.
- Cung cấp các phương thức tiện ích chung: `to_dict`, `display_info`, `__str__`, `__repr__`.
- Các lớp con phải triển khai `employee_type` và `calculate_salary` (đa hình).
"""

from abc import ABC, abstractmethod

from utils.validators import (
    validate_birth_year,
    validate_department_id,
    validate_employee_id,
    validate_full_name,
    validate_non_negative,
)


class Employee(ABC):
    """Nhân viên (lớp trừu tượng).

    Các thuộc tính được khởi tạo qua các validator để đảm bảo dữ liệu hợp lệ.
    """

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0) -> None:
        # Mã nhân viên chỉ đọc (read‑only)
        self.__employee_id = validate_employee_id(employee_id)
        # Các thuộc tính khác được quản lý qua property để kiểm tra
        self.full_name = full_name
        self.birth_year = birth_year
        self.department_id = department_id
        self.base_salary = base_salary

    # ----- property (đóng gói) -----
    @property
    def employee_id(self) -> str:
        """Mã nhân viên – chỉ đọc."""
        return self.__employee_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """Kiểm tra và chuẩn hoá họ tên qua validator."""
        self.__full_name = validate_full_name(value)

    @property
    def birth_year(self) -> int:
        return self.__birth_year

    @birth_year.setter
    def birth_year(self, value: int) -> None:
        """Kiểm tra năm sinh hợp lệ (tuổi 18‑65)."""
        self.__birth_year = validate_birth_year(value)

    @property
    def department_id(self) -> str:
        return self.__department_id

    @department_id.setter
    def department_id(self, value: str) -> None:
        self.__department_id = validate_department_id(value)

    @property
    def base_salary(self) -> float:
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Lương cơ bản không âm."""
        self.__base_salary = validate_non_negative(value, "Lương cơ bản")

    # ----- phương thức trừu tượng (đa hình) -----
    @property
    @abstractmethod
    def employee_type(self) -> str:
        """Tên loại nhân viên, ví dụ 'FullTime' hoặc 'PartTime'."""
        pass

    @abstractmethod
    def calculate_salary(self) -> float:
        """Tính lương – mỗi lớp con ghi đè theo cách riêng."""
        pass

    # ----- tiện ích chung -----
    def to_dict(self) -> dict:
        """Chuyển sang dict để lưu/đọc.
        Các lớp con sẽ mở rộng dict này bằng cách gọi `super().to_dict()`.
        """
        return {
            "type": self.employee_type,
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "birth_year": self.birth_year,
            "department_id": self.department_id,
            "base_salary": self.base_salary,
        }

    def display_info(self) -> None:
        """In thông tin nhân viên ra màn hình (được dùng trong UI)."""
        print(self)

    def __str__(self) -> str:
        """Chuỗi biểu diễn ngắn gọn, dùng trong `print` hoặc logging."""
        return (f"[{self.employee_type}] {self.employee_id} | {self.full_name} | "
                f"{self.birth_year} | {self.department_id} | Lương: {self.calculate_salary():,.0f}")

    def __repr__(self) -> str:
        """Biểu diễn chi tiết cho debugging."""
        return f"{self.__class__.__name__}({self.employee_id!r}, {self.full_name!r})"
