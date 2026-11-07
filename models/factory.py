"""Tạo đối tượng Employee đúng loại từ dict (dùng khi đọc file)."""
from models.employee import Employee
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from utils.exceptions import ValidationError

_REGISTRY = {
    FullTimeEmployee.TYPE: FullTimeEmployee,
    PartTimeEmployee.TYPE: PartTimeEmployee,
}


def employee_from_dict(data: dict) -> Employee:
    """Dựng FullTimeEmployee hoặc PartTimeEmployee dựa trên khóa 'type'."""
    cls = _REGISTRY.get(data.get("type"))
    if cls is None:
        raise ValidationError(f"Loại nhân viên không hợp lệ: {data.get('type')!r}")
    try:
        return cls.from_dict(data)
    except KeyError as exc:
        raise ValidationError(f"Thiếu trường dữ liệu: {exc}") from None
