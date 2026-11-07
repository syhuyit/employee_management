"""Nhân viên bán thời gian."""
from models.employee import Employee
from utils.validators import validate_hours_worked, validate_non_negative


class PartTimeEmployee(Employee):
    """Nhân viên bán thời gian: lương = số giờ làm * đơn giá giờ."""

    TYPE = "PartTime"

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0,
                 hours_worked: float = 0.0, hourly_rate: float = 0.0) -> None:
        super().__init__(employee_id, full_name, birth_year, department_id, base_salary)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    @property
    def hours_worked(self) -> float:
        return self.__hours_worked

    @hours_worked.setter
    def hours_worked(self, value: float) -> None:
        self.__hours_worked = validate_hours_worked(value)

    @property
    def hourly_rate(self) -> float:
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        self.__hourly_rate = validate_non_negative(value, "Đơn giá giờ")

    @property
    def employee_type(self) -> str:
        return self.TYPE

    def calculate_salary(self) -> float:
        return self.hours_worked * self.hourly_rate

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["hours_worked"] = self.hours_worked
        data["hourly_rate"] = self.hourly_rate
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PartTimeEmployee":
        return cls(data["employee_id"], data["full_name"], data["birth_year"],
                   data["department_id"], data.get("base_salary", 0.0),
                   data.get("hours_worked", 0.0), data.get("hourly_rate", 0.0))
