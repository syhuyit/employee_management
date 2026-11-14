"""Lớp trừu tượng Employee - lớp cha của mọi loại nhân viên.

- Thuộc tính được lưu ở dạng private (được tiền tố `__`).
- Truy cập thông qua `@property`/setter để thực hiện kiểm tra dữ liệu.
- `employee_id` chỉ cung cấp getter → thuộc tính chỉ đọc.
- Cung cấp các phương thức tiện ích chung: `to_dict`, `display_info`, `__str__`, `__repr__`.
- Các lớp con phải triển khai `employee_type` và `calculate_salary` (đa hình).
"""  # Docstring mô tả lớp trừu tượng Employee

from abc import ABC, abstractmethod  # Import lớp trừu tượng và decorator abstractmethod

# Import các hàm validator để kiểm tra dữ liệu đầu vào
from utils.validators import (
    validate_birth_year,  # Kiểm tra năm sinh (tuổi 18‑65)
    validate_department_id,  # Kiểm tra mã phòng ban (định dạng ID)
    validate_employee_id,  # Kiểm tra mã nhân viên (ID)
    validate_full_name,  # Kiểm tra và chuẩn hoá họ tên
    validate_non_negative,  # Kiểm tra các giá trị không âm (lương, phụ cấp…)
)


class Employee(ABC):  # Định nghĩa lớp trừu tượng Employee
    """Nhân viên (lớp trừu tượng).

    Các thuộc tính được khởi tạo qua các validator để đảm bảo dữ liệu hợp lệ.
    """  # Docstring cho lớp Employee

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0) -> None:
        # Mã nhân viên chỉ đọc (read‑only)
        self.__employee_id = validate_employee_id(employee_id)  # Áp dụng validator và lưu vào thuộc tính private
        # Các thuộc tính khác được quản lý qua property để kiểm tra
        self.full_name = full_name       # Gọi setter -> validator
        self.birth_year = birth_year     # Gọi setter -> validator
        self.department_id = department_id  # Gọi setter -> validator
        self.base_salary = base_salary   # Gọi setter -> validator

    # ----- property (đóng gói) -----
    @property
    def employee_id(self) -> str:
        """Mã nhân viên – chỉ đọc."""
        return self.__employee_id  # Trả về giá trị private

    @property
    def full_name(self) -> str:
        return self.__full_name  # Truy xuất họ tên đã chuẩn hoá

    @full_name.setter
    def full_name(self, value: str) -> None:
        """Kiểm tra và chuẩn hoá họ tên qua validator."""
        self.__full_name = validate_full_name(value)  # Lưu giá trị đã qua validator

    @property
    def birth_year(self) -> int:
        return self.__birth_year  # Truy xuất năm sinh

    @birth_year.setter
    def birth_year(self, value: int) -> None:
        """Kiểm tra năm sinh hợp lệ (tuổi 18‑65)."""
        self.__birth_year = validate_birth_year(value)  # Lưu giá trị đã qua validator

    @property
    def department_id(self) -> str:
        return self.__department_id  # Truy xuất mã phòng ban

    @department_id.setter
    def department_id(self, value: str) -> None:
        self.__department_id = validate_department_id(value)  # Lưu giá trị đã qua validator

    @property
    def base_salary(self) -> float:
        return self.__base_salary  # Truy xuất lương cơ bản

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Lương cơ bản không âm."""
        self.__base_salary = validate_non_negative(value, "Lương cơ bản")  # Kiểm tra >=0 và lưu

    # ----- phương thức trừu tượng (đa hình) -----
    @property
    @abstractmethod
    def employee_type(self) -> str:
        """Tên loại nhân viên, ví dụ 'FullTime' hoặc 'PartTime'."""
        pass  # Lớp con phải triển khai

    @abstractmethod
    def calculate_salary(self) -> float:
        """Tính lương - mỗi lớp con ghi đè theo cách riêng."""
        pass  # Lớp con phải triển khai

    # ----- tiện ích chung -----
    def to_dict(self) -> dict:
        """Chuyển sang dict để lưu/đọc.
        Các lớp con sẽ mở rộng dict này bằng cách gọi `super().to_dict()`.
        """
        return {
            "type": self.employee_type,          # Loại nhân viên (FullTime/PartTime)
            "employee_id": self.employee_id,      # Mã nhân viên (đã chuẩn hoá)
            "full_name": self.full_name,          # Họ tên chuẩn hoá
            "birth_year": self.birth_year,        # Năm sinh
            "department_id": self.department_id,  # Mã phòng ban
            "base_salary": self.base_salary,      # Lương cơ bản
        }

    def display_info(self) -> None:
        """In thông tin nhân viên ra màn hình (được dùng trong UI)."""
        print(self)  # Gọi __str__ để in thông tin ngắn gọn

    def __str__(self) -> str:
        """Chuỗi biểu diễn ngắn gọn, dùng trong `print` hoặc logging."""
        return (f"[{self.employee_type}] {self.employee_id} | {self.full_name} | "
                f"{self.birth_year} | {self.department_id} | Lương: {self.calculate_salary():,.0f}")

    def __repr__(self) -> str:
        """Biểu diễn chi tiết cho debugging."""
        return f"{self.__class__.__name__}({self.employee_id!r}, {self.full_name!r})"
