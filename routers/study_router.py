from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status

from schemas.study_schema import (
    DeleteStudyResponse,
    GoalCheckResponse,
    StudyRequest,
    StudyResponse,
)
from services.study_service import (
    StudySessionNotFoundError,
    check_goal,
    create_study_session,
    edit_study_session,
    get_study_session_by_id,
    list_study_sessions,
    remove_study_session,
)

router = APIRouter(tags=["Buổi học"])


@router.get("/study/check", response_model=GoalCheckResponse)
def check_study_goal(minutes: Annotated[int, Query(ge=0)]):
    return {"minutes": minutes, "message": check_goal(minutes)}


@router.post(
    "/study/post",
    response_model=StudyResponse,
    status_code=status.HTTP_201_CREATED,
)
def check_study_goal_post(data: StudyRequest):
    return create_study_session(
        name=data.name, topic=data.topic, minutes=data.minutes
    )


@router.get("/study/sessions", response_model=list[StudyResponse])
def get_study_session():
    return list_study_sessions()


@router.get(
    "/study/sessions/{session_id}",
    response_model=StudyResponse,
    responses={404: {"description": "Không tìm thấy buổi học"}},
)
def get_study_session_detail(session_id: Annotated[int, Path(ge=1)]):
    try:
        return get_study_session_by_id(session_id)
    except StudySessionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put(
    "/study/sessions/{session_id}",
    response_model=StudyResponse,
    responses={404: {"description": "Không tìm thấy buổi học"}},
)
def update_study_session_detail(
    session_id: Annotated[int, Path(ge=1)], data: StudyRequest
):
    # PUT nhận đủ ba trường người dùng được phép thay đổi.
    try:
        return edit_study_session(
            session_id=session_id,
            name=data.name,
            topic=data.topic,
            minutes=data.minutes,
        )
    except StudySessionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete(
    "/study/sessions/{session_id}",
    response_model=DeleteStudyResponse,
    responses={404: {"description": "Không tìm thấy buổi học"}},
)
def delete_study_session_detail(session_id: Annotated[int, Path(ge=1)]):
    try:
        return remove_study_session(session_id)
    except StudySessionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
