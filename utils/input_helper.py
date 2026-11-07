"""Hàm nhập liệu console: tự nhập lại khi sai. CHỈ dùng ở tầng ui."""


def input_string(prompt: str, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("[!] Không được để trống, vui lòng nhập lại.")


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("[!] Vui lòng nhập một số nguyên.")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(",", ""))
        except ValueError:
            print("[!] Vui lòng nhập một số.")


def input_choice(prompt: str, valid_choices: list[str]) -> str:
    while True:
        value = input(prompt).strip()
        if value in valid_choices:
            return value
        print(f"[!] Lựa chọn không hợp lệ. Chọn một trong: {', '.join(valid_choices)}")


def confirm(prompt: str) -> bool:
    """Hỏi xác nhận y/n. Trả về True nếu đồng ý."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes", "c", "co", "có"):
            return True
        if answer in ("n", "no", "k", "khong", "không"):
            return False
        print("[!] Vui lòng nhập y hoặc n.")
