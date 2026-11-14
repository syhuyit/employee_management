
"""Handler tìm kiếm và sắp xếp (Gói D)."""

from ui.context import AppContext
from services.search_service import SearchService
from services.sort_service import SortService
from utils.formatter import print_employee_table
from utils.exceptions import ValidationError


def handle_search(ctx: AppContext) -> None:
    """Tìm kiếm nhân viên theo mã hoặc họ tên."""

    while True:
        print("\n========== TÌM KIẾM NHÂN VIÊN ==========")
        print("1. Tìm theo mã nhân viên")
        print("2. Tìm gần đúng theo họ tên")
        print("3. Tìm theo phòng ban")
        print("0. Quay lại")
        print("========================================")

        choice = input("Nhập lựa chọn: ").strip()

        employees = ctx.employee_manager.get_all()

        if choice == "0":
            return

        elif choice == "1":
            employee_id = input("Nhập mã nhân viên cần tìm: ").strip()

            if not employee_id:
                print("Mã nhân viên không được để trống.")
                continue

            result = SearchService.find_by_id(employees, employee_id)

            if result is None:
                print("Không tìm thấy nhân viên phù hợp.")
            else:
                departments = ctx.department_service.get_all()
                department_names = {
                    d.department_id: d.department_name
                    for d in departments
                }
                print_employee_table([result], department_names)

        elif choice == "2":
            keyword = input("Nhập họ tên hoặc từ khóa cần tìm: ").strip()

            if not keyword:
                print("Từ khóa tìm kiếm không được để trống.")
                continue

            results = ctx.employee_manager.search_by_name(keyword)

            if not results:
                print("Không tìm thấy nhân viên phù hợp.")
            else:
                departments = ctx.department_service.get_all()
                department_names = {
                    d.department_id: d.department_name
                    for d in departments
                }
                print_employee_table(results, department_names)

        elif choice == "3":
            department_keyword = input(
                "Nhập mã hoặc tên phòng ban cần tìm: "
            ).strip()

            if not department_keyword:
                print("Thông tin phòng ban không được để trống.")
                continue

            departments = ctx.department_service.get_all()

            # Tìm phòng ban theo mã hoặc tên
            department = next(
                (
                    d for d in departments
                    if d.department_id.casefold() == department_keyword.casefold()
                    or d.department_name.casefold() == department_keyword.casefold()
                ),
                None
            )

            if department is None:
                print("Không tìm thấy phòng ban phù hợp.")
                continue

            results = ctx.employee_manager.search_by_department(
                department.department_id
            )

            if not results:
                print("Không tìm thấy nhân viên phù hợp.")
            else:
                department_names = {
                    d.department_id: d.department_name
                    for d in departments
                }
                print_employee_table(results, department_names)

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


def handle_sort(ctx: AppContext) -> None:
    """Sắp xếp danh sách nhân viên theo tiêu chí."""

    while True:
        print("\n========== SẮP XẾP NHÂN VIÊN ==========")
        print("1. Lương giảm dần")
        print("2. Họ tên tăng dần")
        print("3. Mã nhân viên")
        print("4. Năm sinh")
        print("0. Quay lại")
        print("=======================================")

        choice = input("Nhập lựa chọn: ").strip()

        if choice == "0":
            return

        # Xác định tiêu chí và chiều sắp xếp
        if choice == "1":
            criteria = "salary"
            descending = True

        elif choice == "2":
            criteria = "name"
            descending = False

        elif choice == "3":
            criteria = "id"
            direction = input(
                "Chọn chiều sắp xếp (1. Tăng dần / 2. Giảm dần): "
            ).strip()

            if direction not in ("1", "2"):
                print("Chiều sắp xếp không hợp lệ.")
                continue

            descending = direction == "2"

        elif choice == "4":
            criteria = "birth_year"
            direction = input(
                "Chọn chiều sắp xếp (1. Tăng dần / 2. Giảm dần): "
            ).strip()

            if direction not in ("1", "2"):
                print("Chiều sắp xếp không hợp lệ.")
                continue

            descending = direction == "2"

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            continue

        employees = ctx.employee_manager.get_all()

        if not employees:
            print("(Danh sách nhân viên trống)")
            continue

        try:
            sorted_employees = SortService.sort_employees(
                employees,
                criteria,
                descending
            )

            departments = ctx.department_service.get_all()
            department_names = {
                d.department_id: d.department_name
                for d in departments
            }

            print("\nKẾT QUẢ SAU KHI SẮP XẾP:")
            print_employee_table(sorted_employees, department_names)

        except ValidationError as error:
            print(f"Lỗi sắp xếp: {error}")
