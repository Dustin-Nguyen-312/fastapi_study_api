from repositories.study_repository import (
    add_study_session,
    delete_study_session,
    find_study_session_by_id,
    get_all_study_sessions,
    update_study_session,
)


class StudySessionNotFoundError(LookupError):
    """Lỗi riêng cho tình huống không tìm thấy buổi học."""


def check_goal(minutes: int) -> str:
    if minutes < 0:
        return "Số phút không hợp lệ"
    elif minutes < 30:
        return "Chưa đạt mục tiêu"
    else:
        return "Đã đạt mục tiêu"


def create_study_session(name: str, topic: str, minutes: int):
    session = {
        "name": name,
        "topic": topic,
        "minutes": minutes,
        "message": check_goal(minutes),
    }
    return add_study_session(session)


def list_study_sessions():
    return get_all_study_sessions()


def get_study_session_by_id(session_id: int):
    session = find_study_session_by_id(session_id)

    if session is None:
        raise StudySessionNotFoundError("Không tìm thấy buổi học")

    return session


def edit_study_session(session_id: int, name: str, topic: str, minutes: int):
    # Khi số phút thay đổi, kết luận phải được tính lại.
    new_values = {
        "name": name,
        "topic": topic,
        "minutes": minutes,
        "message": check_goal(minutes),
    }
    updated_session = update_study_session(session_id, new_values)

    if updated_session is None:
        raise StudySessionNotFoundError("Không tìm thấy buổi học")

    return updated_session


def remove_study_session(session_id: int):
    deleted = delete_study_session(session_id)

    if not deleted:
        raise StudySessionNotFoundError("Không tìm thấy buổi học")

    return {"id": session_id, "message": "Đã xóa buổi học"}
