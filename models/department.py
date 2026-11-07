"""Lớp thực thể Department."""
from utils.validators import validate_department_id, validate_department_name


class Department:
    """Phòng ban."""

    def __init__(self, department_id: str, department_name: str) -> None:
        self.__department_id = validate_department_id(department_id)  # chỉ đọc
        self.department_name = department_name

    @property
    def department_id(self) -> str:
        return self.__department_id

    @property
    def department_name(self) -> str:
        return self.__department_name

    @department_name.setter
    def department_name(self, value: str) -> None:
        self.__department_name = validate_department_name(value)

    def to_dict(self) -> dict:
        return {"department_id": self.department_id, "department_name": self.department_name}

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        return cls(data["department_id"], data["department_name"])

    def display_info(self) -> None:
        print(self)

    def __str__(self) -> str:
        return f"{self.department_id} - {self.department_name}"

    def __repr__(self) -> str:
        return f"Department({self.department_id!r}, {self.department_name!r})"
