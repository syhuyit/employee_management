"""Nhân viên bán thời gian.

Lớp PartTimeEmployee kế thừa Employee và bổ sung các thuộc tính đặc thù
`hours_worked` (số giờ làm) và `hourly_rate` (đơn giá giờ).
"""

from models.employee import Employee  # Lớp cha Employee
from utils.validators import validate_hours_worked, validate_non_negative  # Validators


class PartTimeEmployee(Employee):
    """Nhân viên bán thời gian: lương = số giờ làm * đơn giá giờ.

    Thuộc tính đặc thù:
    - `hours_worked`: số giờ làm, phải trong khoảng 0‑MAX_HOURS_WORKED.
    - `hourly_rate`: đơn giá giờ, không âm.
    """

    TYPE = "PartTime"  # Hằng số xác định loại nhân viên

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0,
                 hours_worked: float = 0.0, hourly_rate: float = 0.0) -> None:
        # Gọi khởi tạo lớp cha để thiết lập các thuộc tính chung
        super().__init__(employee_id, full_name, birth_year, department_id, base_salary)
        # Thiết lập giờ làm và đơn giá giờ qua setter để kiểm tra
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    @property
    def hours_worked(self) -> float:
        """Trả về số giờ làm đã chuẩn hoá (private)."""
        return self.__hours_worked

    @hours_worked.setter
    def hours_worked(self, value: float) -> None:
        """Kiểm tra số giờ làm (0-MAX_HOURS_WORKED) và lưu.
        
        Sử dụng validator `validate_hours_worked`.
        """
        self.__hours_worked = validate_hours_worked(value)

    @property
    def hourly_rate(self) -> float:
        """Trả về đơn giá giờ đã chuẩn hoá (private)."""
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        """Kiểm tra đơn giá giờ không âm và lưu.
        
        Sử dụng validator `validate_non_negative`.
        """
        self.__hourly_rate = validate_non_negative(value, "Đơn giá giờ")

    @property
    def employee_type(self) -> str:
        """Trả về loại nhân viên (PartTime)."""
        return self.TYPE

    def calculate_salary(self) -> float:
        """Tính lương: số giờ làm * đơn giá giờ."""
        return self.hours_worked * self.hourly_rate

    def __str__(self) -> str:
        """Hiển thị thông tin đầy đủ cho nhân viên bán thời gian, bao gồm số giờ và đơn giá.
        
        Gọi `__str__` của lớp cha rồi nối thêm thông tin.
        """
        base_str = super().__str__()  # Chuỗi cơ bản từ Employee
        return f"{base_str} | Giờ: {self.hours_worked:g} | Đơn giá: {self.hourly_rate:,.0f}"

    def to_dict(self) -> dict:
        """Chuyển đối tượng PartTimeEmployee sang dict, bao gồm các trường đặc thù."""
        data = super().to_dict()
        data["hours_worked"] = self.hours_worked
        data["hourly_rate"] = self.hourly_rate
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PartTimeEmployee":
        """Tạo PartTimeEmployee từ dict.
        
        Các trường được đọc từ dict, sử dụng giá trị mặc định nếu không có.
        """
        return cls(
            data["employee_id"],
            data["full_name"],
            data["birth_year"],
            data["department_id"],
            data.get("base_salary", 0.0),
            data.get("hours_worked", 0.0),
            data.get("hourly_rate", 0.0),
        )
