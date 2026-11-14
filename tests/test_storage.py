"""Unit test cho FileStorage (Goi E). Dung tempfile, khong dong vao data/ that."""
import json
import os
import tempfile
import unittest

from models.department import Department
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from storage.file_storage import FileStorage
from utils.exceptions import StorageError  # xem luu y so 2


def _make_data():
    departments = [
        Department(department_id="PB01", department_name="Kỹ thuật"),
        Department(department_id="PB02", department_name="Kinh doanh"),
    ]
    employees = [
        FullTimeEmployee(
            employee_id="NV01", full_name="Nguyễn Văn An", birth_year=1995,
            department_id="PB01", base_salary=10_000_000, allowance=2_000_000,
        ),
        PartTimeEmployee(
            employee_id="NV02", full_name="Trần Thị Bình", birth_year=2001,
            department_id="PB02", base_salary=0, hours_worked=80, hourly_rate=50_000,
        ),
    ]
    return employees, departments


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp_dir = tmp.name
        self.path = os.path.join(self.tmp_dir, "company_data.json")
        self.storage = FileStorage(self.path)

    def _write_raw(self, text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    # ---- save ----
    def test_save_creates_file(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        self.assertTrue(self.storage.exists())

    def test_save_creates_missing_directory(self):
        nested = os.path.join(self.tmp_dir, "data", "sub", "x.json")
        storage = FileStorage(nested)
        employees, departments = _make_data()
        storage.save(employees, departments)
        self.assertTrue(os.path.exists(nested))

    def test_save_json_structure(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(set(data.keys()), {"departments", "employees"})
        self.assertEqual(len(data["departments"]), 2)
        self.assertEqual(len(data["employees"]), 2)

    def test_save_keeps_vietnamese_unescaped(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        with open(self.path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("Nguyễn Văn An", text)
        self.assertNotIn("\\u", text)

    def test_save_leaves_no_temp_file(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        self.assertEqual(os.listdir(self.tmp_dir), ["company_data.json"])

    def test_save_overwrites_old_data(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        self.storage.save(employees[:1], departments[:1])
        loaded_emp, loaded_dep = self.storage.load()
        self.assertEqual(len(loaded_emp), 1)
        self.assertEqual(len(loaded_dep), 1)

    def test_save_io_error_raises_storage_error(self):
        # file_path tro vao mot thu muc -> khong the ghi/replace
        storage = FileStorage(self.tmp_dir)
        employees, departments = _make_data()
        with self.assertRaises(StorageError):
            storage.save(employees, departments)

    # ---- load ----
    def test_load_missing_file_returns_empty(self):
        self.assertFalse(self.storage.exists())
        self.assertEqual(self.storage.load(), ([], []))

    def test_save_then_load_roundtrip(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        loaded_emp, loaded_dep = self.storage.load()
        self.assertEqual([e.to_dict() for e in loaded_emp], [e.to_dict() for e in employees])
        self.assertEqual([d.to_dict() for d in loaded_dep], [d.to_dict() for d in departments])

    def test_load_restores_correct_classes(self):
        employees, departments = _make_data()
        self.storage.save(employees, departments)
        loaded_emp, _ = self.storage.load()
        self.assertIsInstance(loaded_emp[0], FullTimeEmployee)
        self.assertIsInstance(loaded_emp[1], PartTimeEmployee)
        self.assertEqual(loaded_emp[0].calculate_salary(), employees[0].calculate_salary())

    def test_save_empty_then_load_empty(self):
        self.storage.save([], [])
        self.assertEqual(self.storage.load(), ([], []))

    def test_load_corrupted_json_raises_storage_error(self):
        self._write_raw("{ day khong phai json hop le ")
        with self.assertRaises(StorageError):
            self.storage.load()

    def test_load_empty_file_raises_storage_error(self):
        self._write_raw("")
        with self.assertRaises(StorageError):
            self.storage.load()

    def test_load_wrong_root_type_raises_storage_error(self):
        self._write_raw("[1, 2, 3]")
        with self.assertRaises(StorageError):
            self.storage.load()

    def test_load_missing_key_raises_storage_error(self):
        self._write_raw(json.dumps({"departments": []}))
        with self.assertRaises(StorageError):
            self.storage.load()

    def test_load_invalid_employee_data_raises_storage_error(self):
        self._write_raw(json.dumps({
            "departments": [],
            "employees": [{"employee_id": "NV01"}],  # thieu rat nhieu truong
        }))
        with self.assertRaises(StorageError):
            self.storage.load()


if __name__ == "__main__":
    unittest.main()