"""Unit tests for utils.validators.

Các test này kiểm tra các hàm validate_* để đảm bảo đáp ứng các ràng buộc biên.
"""

import math
import pytest
from utils.validators import (
    validate_identifier,
    validate_full_name,
    validate_birth_year,
    validate_number,
    validate_non_negative,
    validate_hours_worked,
)
from utils.exceptions import ValidationError

# ---------------------------------------------------------------------------
# Mã định danh
# ---------------------------------------------------------------------------

def test_validate_identifier_success():
    assert validate_identifier("abc") == "ABC"
    assert validate_identifier("Nv001") == "NV001"


def test_validate_identifier_errors():
    # Độ dài < 3
    with pytest.raises(ValidationError):
        validate_identifier("ab")
    # Độ dài > 10
    with pytest.raises(ValidationError):
        validate_identifier("ABCDEFGHIJK")
    # Khoảng trắng
    with pytest.raises(ValidationError):
        validate_identifier("NV 001")
    # Dấu '-'
    with pytest.raises(ValidationError):
        validate_identifier("NV-001")

# ---------------------------------------------------------------------------
# Họ tên
# ---------------------------------------------------------------------------

def test_validate_full_name_success():
    assert validate_full_name("  Nguyễn   Văn  An ") == "Nguyễn Văn An"
    assert validate_full_name("Lê Thị B") == "Lê Thị B"


def test_validate_full_name_errors():
    # Rỗng
    with pytest.raises(ValidationError):
        validate_full_name("")
    # Toàn khoảng trắng
    with pytest.raises(ValidationError):
        validate_full_name("   ")
    # 1 ký tự
    with pytest.raises(ValidationError):
        validate_full_name("A")
    # Chứa số
    with pytest.raises(ValidationError):
        validate_full_name("An123")

# ---------------------------------------------------------------------------
# Năm sinh
# ---------------------------------------------------------------------------

def test_validate_birth_year_success():
    # Giả sử năm hiện tại 2026, tuổi 18 và 65 hợp lệ
    current_year = 2026
    assert validate_birth_year(current_year - 18) == current_year - 18
    assert validate_birth_year(current_year - 65) == current_year - 65


def test_validate_birth_year_errors():
    current_year = 2026
    # Tuổi < 18
    with pytest.raises(ValidationError):
        validate_birth_year(current_year - 17)
    # Tuổi > 65
    with pytest.raises(ValidationError):
        validate_birth_year(current_year - 66)
    # Kiểu chuỗi
    with pytest.raises(ValidationError):
        validate_birth_year("1990")
    # Kiểu bool
    with pytest.raises(ValidationError):
        validate_birth_year(True)

# ---------------------------------------------------------------------------
# Số (number) và các hàm dựa trên nó
# ---------------------------------------------------------------------------

def test_validate_number_success_and_limits():
    # Giá trị hợp lệ trong khoảng
    assert validate_number(10, "Test", 0, 20) == 10.0
    # Giá trị min
    assert validate_number(0, "Test", 0) == 0.0
    # Giá trị max
    assert validate_number(20, "Test", 0, 20) == 20.0


def test_validate_number_errors():
    # Bool
    with pytest.raises(ValidationError):
        validate_number(True, "Test")
    # Không chuyển được thành float
    with pytest.raises(ValidationError):
        validate_number("abc", "Test")
    # NaN / Inf
    with pytest.raises(ValidationError):
        validate_number(float('nan'), "Test")
    with pytest.raises(ValidationError):
        validate_number(float('inf'), "Test")
    # Dưới min_value
    with pytest.raises(ValidationError):
        validate_number(-1, "Test", 0)
    # Trên max_value
    with pytest.raises(ValidationError):
        validate_number(101, "Test", 0, 100)

# ---------------------------------------------------------------------------
# Các hàm tiện ích dựa trên validate_number
# ---------------------------------------------------------------------------

def test_validate_non_negative():
    assert validate_non_negative(0, "Lương") == 0.0
    assert validate_non_negative(123.45, "Lương") == 123.45
    with pytest.raises(ValidationError):
        validate_non_negative(-5, "Lương")


def test_validate_hours_worked():
    # Giới hạn 0‑300
    assert validate_hours_worked(0) == 0.0
    assert validate_hours_worked(300) == 300.0
    with pytest.raises(ValidationError):
        validate_hours_worked(301)
    with pytest.raises(ValidationError):
        validate_hours_worked(-1)
"
