from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: datetime = datetime.now()
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None