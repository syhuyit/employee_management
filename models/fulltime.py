"""Nhân viên toàn thời gian."""
from models.employee import Employee
from utils.validators import validate_non_negative


class FullTimeEmployee(Employee):
    """Nhân viên toàn thời gian: lương = lương cơ bản + phụ cấp."""

    TYPE = "FullTime"

    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0, allowance: float = 0.0) -> None:
        super().__init__(employee_id, full_name, birth_year, department_id, base_salary)
        self.allowance = allowance

    @property
    def allowance(self) -> float:
        return self.__allowance

    @allowance.setter
    def allowance(self, value: float) -> None:
        self.__allowance = validate_non_negative(value, "Phụ cấp")

    @property
    def employee_type(self) -> str:
        return self.TYPE

    def calculate_salary(self) -> float:
        return self.base_salary + self.allowance

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["allowance"] = self.allowance
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "FullTimeEmployee":
        return cls(data["employee_id"], data["full_name"], data["birth_year"],
                   data["department_id"], data.get("base_salary", 0.0), data.get("allowance", 0.0))
