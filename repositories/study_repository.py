import csv
import os
import tempfile
from pathlib import Path
from threading import Lock


# Tính đường dẫn theo vị trí file code, không theo thư mục Terminal đang đứng.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "study_sessions.csv"
FIELDNAMES = ["id", "name", "topic", "minutes", "message"]

# Các request trong cùng một tiến trình không được ghi CSV chồng lên nhau.
_file_lock = Lock()


def _read_sessions():
    """Hàm hỗ trợ đọc CSV. Các hàm bên dưới gọi nó trong vùng có khóa."""
    if not DATA_FILE.exists():
        return []

    sessions = []
    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("Header CSV không đúng cấu trúc buổi học")

        seen_ids = set()
        for row in reader:
            # CSV đọc các ô thành chuỗi; chuyển hai trường số về int.
            session = {
                "id": int(row["id"]),
                "name": row["name"],
                "topic": row["topic"],
                "minutes": int(row["minutes"]),
                "message": row["message"],
            }
            if session["id"] < 1 or session["id"] in seen_ids:
                raise ValueError("ID trong CSV không hợp lệ hoặc bị trùng")
            if session["minutes"] < 0:
                raise ValueError("Số phút trong CSV không hợp lệ")
            seen_ids.add(session["id"])
            sessions.append(session)

    return sessions


def _write_sessions(sessions):
    """Ghi file tạm xong mới thay CSV để lỗi lúc ghi không cắt mất file cũ."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=DATA_FILE.parent, prefix="study_", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(sessions)
        os.replace(temporary_name, DATA_FILE)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def get_all_study_sessions():
    with _file_lock:
        return _read_sessions()


def add_study_session(session: dict):
    with _file_lock:
        sessions = _read_sessions()

        max_id = 0
        for saved_session in sessions:
            if saved_session["id"] > max_id:
                max_id = saved_session["id"]

        new_session = session.copy()
        new_session["id"] = max_id + 1
        sessions.append(new_session)
        _write_sessions(sessions)
        return new_session


def find_study_session_by_id(session_id: int):
    with _file_lock:
        sessions = _read_sessions()
        for session in sessions:
            if session["id"] == session_id:
                return session
        return None


def update_study_session(session_id: int, new_values: dict):
    with _file_lock:
        sessions = _read_sessions()
        for index, session in enumerate(sessions):
            if session["id"] == session_id:
                updated_session = {
                    "id": session_id,
                    "name": new_values["name"],
                    "topic": new_values["topic"],
                    "minutes": new_values["minutes"],
                    "message": new_values["message"],
                }
                sessions[index] = updated_session
                _write_sessions(sessions)
                return updated_session
        return None


def delete_study_session(session_id: int):
    with _file_lock:
        sessions = _read_sessions()
        for index, session in enumerate(sessions):
            if session["id"] == session_id:
                sessions.pop(index)
                _write_sessions(sessions)
                return True
        return False
