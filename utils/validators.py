"""Các hàm kiểm tra dữ liệu đầu vào. Trả về giá trị đã chuẩn hóa hoặc ném ValidationError."""
import math
import re
from datetime import date

from utils.exceptions import ValidationError

MIN_AGE = 18
MAX_AGE = 65
MAX_HOURS_WORKED = 300
_ID_PATTERN = re.compile(r"^[A-Z0-9]{3,10}$")


def validate_not_empty(value, field_name: str) -> str:
    """Kiểm tra một chuỗi không rỗng.
    - Nếu `value` là `None` hoặc chuỗi chỉ chứa khoảng trắng → ném `ValidationError`.
    - Trả về chuỗi đã `strip()` (loại bỏ khoảng trắng đầu và cuối).
    """
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} không được để trống.")
    return str(value).strip()



def validate_identifier(value, field_name: str = "Mã") -> str:
    """Xác thực mã định danh.

    - Không cho phép chuỗi rỗng hoặc chứa khoảng trắng.
    - Chỉ chấp nhận các ký tự chữ in hoa A‑Z và chữ số 0‑9.
    - Độ dài phải nằm trong khoảng 3‑10 ký tự (đúng biên 3 và 10 được chấp nhận).
    - Trả về giá trị đã chuẩn hoá thành chữ in hoa.
    """
    # Loại bỏ khoảng trắng đầu/cuối, sau đó chuẩn hoá thành chữ in hoa
    text = validate_not_empty(value, field_name).upper()
    # Kiểm tra định dạng theo pattern đã định nghĩa ở đầu file
    if not _ID_PATTERN.match(text):
        raise ValidationError(
            f"{field_name} chỉ gồm chữ/số, dài 3 đến 10 ký tự, không có dấu cách hay ký tự '-' (ví dụ: NV001)."
        )
    return text



def validate_employee_id(value) -> str:
    return validate_identifier(value, "Mã nhân viên")


def validate_department_id(value) -> str:
    return validate_identifier(value, "Mã phòng ban")


def validate_full_name(value) -> str:
    """Họ tên 2-50 ký tự, chỉ chữ cái và khoảng trắng."""
    text = " ".join(validate_not_empty(value, "Họ tên").split())
    if not 2 <= len(text) <= 50:
        raise ValidationError("Họ tên phải dài từ 2 đến 50 ký tự.")
    if not all(ch.isalpha() or ch == " " for ch in text):
        raise ValidationError("Họ tên chỉ được chứa chữ cái và khoảng trắng.")
    return text


def validate_department_name(value) -> str:
    """Tên phòng ban 2-50 ký tự."""
    text = " ".join(validate_not_empty(value, "Tên phòng ban").split())
    if not 2 <= len(text) <= 50:
        raise ValidationError("Tên phòng ban phải dài từ 2 đến 50 ký tự.")
    return text


def validate_birth_year(value) -> int:
    """Năm sinh là số nguyên, tuổi trong khoảng MIN_AGE..MAX_AGE."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError("Năm sinh phải là số nguyên.")
    current_year = date.today().year
    if not (current_year - MAX_AGE <= value <= current_year - MIN_AGE):
        raise ValidationError(
            f"Năm sinh phải trong khoảng {current_year - MAX_AGE} đến {current_year - MIN_AGE} "
            f"(tuổi từ {MIN_AGE} đến {MAX_AGE})."
        )
    return value


def validate_number(value, field_name: str, min_value: float = 0.0, max_value: float | None = None) -> float:
    """Kiểm tra số thực trong khoảng [min_value, max_value]."""
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} phải là số.")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} phải là số.") from None
    if not math.isfinite(number):
        raise ValidationError(f"{field_name} không hợp lệ.")
    if number < min_value:
        raise ValidationError(f"{field_name} phải >= {min_value:g}.")
    if max_value is not None and number > max_value:
        raise ValidationError(f"{field_name} phải <= {max_value:g}.")
    return number


def validate_non_negative(value, field_name: str) -> float:
    """Số không âm (dùng cho lương, phụ cấp, đơn giá giờ)."""
    return validate_number(value, field_name, 0.0)


def validate_hours_worked(value) -> float:
    """Số giờ làm từ 0 đến MAX_HOURS_WORKED."""
    return validate_number(value, "Số giờ làm", 0.0, MAX_HOURS_WORKED)
