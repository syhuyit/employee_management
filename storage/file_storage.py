"""Luu/doc du lieu ra file JSON (chuc nang mo rong)."""
import json
import os

from models.department import Department
from models.employee import Employee
from models.factory import employee_from_dict
from utils.exceptions import StorageError  # xem luu y so 1 ben duoi


class FileStorage:
    """Luu va doc danh sach nhan vien + phong ban."""

    def __init__(self, file_path: str = "data/company_data.json") -> None:
        self.file_path = file_path

    def exists(self) -> bool:
        return os.path.exists(self.file_path)

    def save(self, employees: list[Employee], departments: list[Department]) -> None:
        """Ghi JSON an toan (file tam + os.replace). Loi I/O -> StorageError."""
        tmp_path = self.file_path + ".tmp"
        try:
            # Tu tao thu muc cha (vi du data/) neu chua co
            folder = os.path.dirname(self.file_path)
            if folder:
                os.makedirs(folder, exist_ok=True)

            payload = {
                "departments": [d.to_dict() for d in departments],
                "employees": [e.to_dict() for e in employees],
            }
            # Ghi file tam truoc, thanh cong het moi thay the file that
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.file_path)
        except (OSError, TypeError, ValueError) as exc:
            # Don file tam neu con sot lai
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass
            raise StorageError(f"Khong the luu file '{self.file_path}': {exc}") from exc

    def load(self) -> tuple[list[Employee], list[Department]]:
        """Doc JSON. File chua co -> ([], []). File hong/sai du lieu -> StorageError."""
        if not self.exists():
            return [], []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as exc:
            # JSONDecodeError va UnicodeDecodeError deu la con cua ValueError
            raise StorageError(f"Khong the doc file '{self.file_path}': {exc}") from exc

        if (
            not isinstance(data, dict)
            or not isinstance(data.get("departments"), list)
            or not isinstance(data.get("employees"), list)
        ):
            raise StorageError(
                "Cau truc file khong hop le: can {'departments': [...], 'employees': [...]}"
            )

        try:
            # Phong ban truoc, nhan vien sau
            departments = [Department.from_dict(d) for d in data["departments"]]
            employees = [employee_from_dict(e) for e in data["employees"]]
        except Exception as exc:
            # Du lieu sai (thieu truong, sai kieu, vi pham validate...) -> khong de sap chuong trinh
            raise StorageError(f"Du lieu trong file khong hop le: {exc}") from exc

        return employees, departments