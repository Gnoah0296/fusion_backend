from fastapi import FastAPI

from database.db import init_db
from database.seed import seed_system_admin
from routers import users, projects, tasks

app = FastAPI(title="FUSION ? Multi-Enterprise IT Project Maintenance & Development Platform")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_system_admin()
