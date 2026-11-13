"""Nhân viên toàn thời gian.

Lớp FullTimeEmployee kế thừa Employee và bổ sung phụ cấp (allowance).
"""

from models.employee import Employee  # Import lớp cha Employee
from utils.validators import validate_non_negative  # Validator cho phụ cấp không âm


class FullTimeEmployee(Employee):
    """Nhân viên toàn thời gian: lương = lương cơ bản + phụ cấp.
    
    Thuộc tính đặc thù:
    - `allowance`: phụ cấp, không âm.
    """

    TYPE = "FullTime"  # Hằng số xác định loại nhân viên

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0, allowance: float = 0.0) -> None:
        # Gọi khởi tạo lớp cha để thiết lập các thuộc tính chung
        super().__init__(employee_id, full_name, birth_year, department_id, base_salary)
        # Thiết lập phụ cấp thông qua setter để thực hiện kiểm tra
        self.allowance = allowance

    @property
    def allowance(self) -> float:
        """Trả về phụ cấp đã chuẩn hoá (private)."""
        return self.__allowance

    @allowance.setter
    def allowance(self, value: float) -> None:
        """Kiểm tra phụ cấp không âm và lưu vào thuộc tính private."""
        self.__allowance = validate_non_negative(value, "Phụ cấp")

    @property
    def employee_type(self) -> str:
        """Trả về loại nhân viên (FullTime)."""
        return self.TYPE

    def calculate_salary(self) -> float:
        """Tính lương: lương cơ bản + phụ cấp."""
        return self.base_salary + self.allowance

    def __str__(self) -> str:
        """Hiển thị thông tin đầy đủ, bao gồm phụ cấp.
        
        Gọi __str__ của lớp cha rồi nối thêm thông tin phụ cấp.
        """
        base_str = super().__str__()  # Chuỗi cơ bản từ Employee
        return f"{base_str} | Phụ cấp: {self.allowance:,.0f}"

    def to_dict(self) -> dict:
        """Chuyển đối tượng FullTimeEmployee sang dict.
        Bao gồm các trường của Employee và trường `allowance`.
        """
        data = super().to_dict()  # Lấy dict cơ bản từ Employee
        data["allowance"] = self.allowance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "FullTimeEmployee":
        """Tạo FullTimeEmployee từ dict.
        
        Các trường được đọc từ dict, sử dụng giá trị mặc định nếu không có.
        """
        return cls(
            data["employee_id"],
            data["full_name"],
            data["birth_year"],
            data["department_id"],
            data.get("base_salary", 0.0),
            data.get("allowance", 0.0),
        )
