from fastapi import FastAPI
from database.db import Base, engine
from routers.user_router import router as user_router
from routers.project_router import router as project_router
from routers.task_router import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(project_router)
app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def home():
    return {"message": "Fusion backend is running!"}
