from database.db import Base, engine
from database.models import user, project, project_member, task

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
