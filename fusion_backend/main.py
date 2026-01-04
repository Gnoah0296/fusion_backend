from fastapi import FastAPI
from database.db import Base, engine
from routers.project_router import router as project_router
from database.models import project
from routers.task_router import router as task_router
from routers.user_router import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(project_router)

app.include_router(task_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Fusion Backend Running"}

