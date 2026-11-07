"""Lớp trừu tượng Employee – lớp cha của mọi loại nhân viên."""
from abc import ABC, abstractmethod

from utils.validators import (
    validate_birth_year,
    validate_department_id,
    validate_employee_id,
    validate_full_name,
    validate_non_negative,
)


class Employee(ABC):
    """Nhân viên (lớp trừu tượng). Thuộc tính private, truy cập qua property."""

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0) -> None:
        self.__employee_id = validate_employee_id(employee_id)  # chỉ đọc (R14)
        self.full_name = full_name
        self.birth_year = birth_year
        self.department_id = department_id
        self.base_salary = base_salary

    # ----- property (đóng gói) -----
    @property
    def employee_id(self) -> str:
        return self.__employee_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self.__full_name = validate_full_name(value)

    @property
    def birth_year(self) -> int:
        return self.__birth_year

    @birth_year.setter
    def birth_year(self, value: int) -> None:
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
        self.__base_salary = validate_non_negative(value, "Lương cơ bản")

    # ----- phương thức trừu tượng (đa hình) -----
    @property
    @abstractmethod
    def employee_type(self) -> str:
        """Tên loại nhân viên, ví dụ 'FullTime'."""

    @abstractmethod
    def calculate_salary(self) -> float:
        """Tính lương – mỗi lớp con ghi đè theo cách riêng."""

    # ----- tiện ích chung -----
    def to_dict(self) -> dict:
        """Chuyển thành dict để lưu file. Lớp con gọi super().to_dict() rồi bổ sung."""
        return {
            "type": self.employee_type,
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "birth_year": self.birth_year,
            "department_id": self.department_id,
            "base_salary": self.base_salary,
        }

    def display_info(self) -> None:
        """In thông tin nhân viên ra màn hình."""
        print(self)

    def __str__(self) -> str:
        return (f"[{self.employee_type}] {self.employee_id} | {self.full_name} | "
                f"{self.birth_year} | {self.department_id} | Lương: {self.calculate_salary():,.0f}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.employee_id!r}, {self.full_name!r})"
