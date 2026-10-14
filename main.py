from fastapi import FastAPI

from routers.study_router import router

app = FastAPI(title="API quản lý buổi học", version="1.0.0")
app.include_router(router)
