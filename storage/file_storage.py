"""Lưu/đọc dữ liệu ra file JSON (chức năng mở rộng)."""
import os

from models.department import Department
from models.employee import Employee


class FileStorage:
    """Lưu và đọc danh sách nhân viên + phòng ban."""

    def __init__(self, file_path: str = "data/company_data.json") -> None:
        self.file_path = file_path

    def exists(self) -> bool:
        return os.path.exists(self.file_path)

    def save(self, employees: list[Employee], departments: list[Department]) -> None:
        """[BASE-MIN] Chưa làm gì. TODO(Gói E): ghi JSON an toàn, lỗi -> StorageError."""

    def load(self) -> tuple[list[Employee], list[Department]]:
        """[BASE-MIN] Trả về hai danh sách rỗng. TODO(Gói E): đọc JSON, dùng employee_from_dict."""
        return [], []
