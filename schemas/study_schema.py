from pydantic import BaseModel, ConfigDict, Field


class StudyRequest(BaseModel):
    # Bỏ khoảng trắng đầu/cuối trước khi kiểm tra độ dài.
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    minutes: int = Field(ge=0)


class StudyResponse(BaseModel):
    id: int = Field(ge=1)
    name: str
    topic: str
    minutes: int = Field(ge=0)
    message: str


class GoalCheckResponse(BaseModel):
    # Chỉ kiểm tra mục tiêu, không tạo bản ghi nên không có ID.
    minutes: int
    message: str


class DeleteStudyResponse(BaseModel):
    id: int
    message: str
