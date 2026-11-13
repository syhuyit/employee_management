"""Unit tests for employee models.

Các test này kiểm tra:
- Lớp `Employee` là abstract và không thể khởi tạo.
- `FullTimeEmployee` và `PartTimeEmployee` tính lương đúng.
- Đa hình: danh sách các đối tượng khác nhau đều có thể gọi `calculate_salary`.
- Các setter báo `ValidationError` khi dữ liệu không hợp lệ.
- `to_dict` / `from_dict` / `employee_from_dict` trả về đối tượng cùng lớp và cùng lương.
- Kiểm tra các ràng buộc biên đã định nghĩa trong `validators`.
"""

from datetime import date

import pytest
from utils.exceptions import ValidationError
from utils.validators import (
    validate_identifier,
    validate_full_name,
    validate_birth_year,
    validate_hours_worked,
    validate_non_negative,
)
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from models.employee import Employee
from models.factory import employee_from_dict

# ---------------------------------------------------------------------------
# A2 – Abstract class
# ---------------------------------------------------------------------------

def test_employee_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Employee("NV001", "Nguyen Van A", 1990, "PB01", 1000.0)

# ---------------------------------------------------------------------------
# A3 – FullTimeEmployee salary
# ---------------------------------------------------------------------------

def test_fulltime_salary_calculation():
    emp = FullTimeEmployee("NV001", "Nguyen Van A", 1990, "PB01", 15000000, 2000000)
    assert emp.calculate_salary() == 17000000
    # __str__ contains allowance
    assert "Phụ cấp: 2,000,000" in str(emp)

# ---------------------------------------------------------------------------
# A4 – PartTimeEmployee salary
# ---------------------------------------------------------------------------

def test_parttime_salary_calculation():
    emp = PartTimeEmployee("NV002", "Le Thi B", 1995, "PB02", 0.0, hours_worked=40, hourly_rate=200000)
    assert emp.calculate_salary() == 8000000
    # __str__ contains hours and rate
    assert "Giờ: 40" in str(emp) and "Đơn giá: 200,000" in str(emp)

# ---------------------------------------------------------------------------
# A5 – Dict round‑trip and factory
# ---------------------------------------------------------------------------

def test_fulltime_dict_roundtrip():
    original = FullTimeEmployee("NV003", "Tran Van C", 1985, "PB03", 12000000, 1500000)
    data = original.to_dict()
    restored = employee_from_dict(data)
    assert isinstance(restored, FullTimeEmployee)
    assert restored.calculate_salary() == original.calculate_salary()

def test_parttime_dict_roundtrip():
    original = PartTimeEmployee("NV004", "Pham D", 1992, "PB04", 0.0, 30, 250000)
    data = original.to_dict()
    restored = employee_from_dict(data)
    assert isinstance(restored, PartTimeEmployee)
    assert restored.calculate_salary() == original.calculate_salary()

def test_factory_invalid_type():
    with pytest.raises(ValidationError):
        employee_from_dict({"type": "Unknown", "employee_id": "NV005"})

def test_factory_missing_field():
    data = {"type": "FullTime", "employee_id": "NV006"}
    with pytest.raises(ValidationError):
        employee_from_dict(data)

# ---------------------------------------------------------------------------
# A6 – Setter validation (boundary cases)
# ---------------------------------------------------------------------------

def test_setters_validation_errors():
    emp = FullTimeEmployee("NV007", "Hoang E", 1990, "PB05", 1000000, 500000)
    current_year = date.today().year
    # employee_id is read‑only
    with pytest.raises(AttributeError):
        emp.employee_id = "NV999"
    # full_name invalid
    with pytest.raises(ValidationError):
        emp.full_name = "A1"
    # birth_year invalid (too young)
    with pytest.raises(ValidationError):
        emp.birth_year = current_year - 17
    # department_id invalid
    with pytest.raises(ValidationError):
        emp.department_id = "ab"
    # base_salary negative
    with pytest.raises(ValidationError):
        emp.base_salary = -1000
    # allowance negative via subclass setter
    with pytest.raises(ValidationError):
        emp.allowance = -500


def test_fulltime_zero_allowance_keeps_base_salary():
    emp = FullTimeEmployee("NV008", "Hoang F", 1990, "PB05", 1000000, 0)

    assert emp.allowance == 0
    assert emp.calculate_salary() == 1000000


def test_parttime_zero_hours_results_in_zero_salary():
    emp = PartTimeEmployee("NV009", "Tran G", 1990, "PB05", 0, 0, 200000)

    assert emp.calculate_salary() == 0


def test_parttime_hours_setter_rejects_value_above_limit():
    emp = PartTimeEmployee("NV010", "Le H", 1990, "PB05", 0, 40, 200000)

    with pytest.raises(ValidationError):
        emp.hours_worked = 301

# ---------------------------------------------------------------------------
# Additional boundary tests using validators directly (already covered in test_validators)
# ---------------------------------------------------------------------------

def test_identifier_boundary():
    # exact min length
    assert validate_identifier("abc") == "ABC"
    # exact max length (10)
    assert validate_identifier("ABCDEFGHIJ") == "ABCDEFGHIJ"
    # too long
    with pytest.raises(ValidationError):
        validate_identifier("ABCDEFGHIJK")

def test_full_name_boundary():
    # minimum length 2
    assert validate_full_name("An") == "An"
    # leading/trailing spaces are stripped and collapsed
    assert validate_full_name("  An   B ") == "An B"
    # too short
    with pytest.raises(ValidationError):
        validate_full_name("A")

def test_birth_year_boundary():
    current = date.today().year
    # exactly 18 years old
    assert validate_birth_year(current - 18) == current - 18
    # exactly 65 years old
    assert validate_birth_year(current - 65) == current - 65
    # below
    with pytest.raises(ValidationError):
        validate_birth_year(current - 17)
    # above
    with pytest.raises(ValidationError):
        validate_birth_year(current - 66)

def test_hours_worked_boundary():
    # 0 and max
    assert validate_hours_worked(0) == 0.0
    assert validate_hours_worked(300) == 300.0
    # beyond max
    with pytest.raises(ValidationError):
        validate_hours_worked(301)

