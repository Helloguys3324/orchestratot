from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum
from typing import List

app = FastAPI()

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO

# In-memory storage for testing
tasks_db: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task