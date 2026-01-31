from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models.todo import TodoItem, TodoStatus, Priority
from services.todo_service import TodoService
import uvicorn


app = FastAPI(title="Todo List API", description="A modern Todo List API built with FastAPI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the todo service
todo_service = TodoService()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo List API"}


@app.get("/todos/", response_model=List[TodoItem])
def get_todos():
    """Get all todos"""
    return todo_service.get_all_todos()


@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    """Create a new todo"""
    # Reset ID to None to let the service assign a new one
    todo.id = None
    return todo_service.create_todo(todo)


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo: TodoItem):
    """Update an existing todo"""
    existing_todo = todo_service.get_todo_by_id(todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Ensure the ID matches
    todo.id = todo_id
    updated_todo = todo_service.update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@app.patch("/todos/{todo_id}/toggle-status", response_model=TodoItem)
def toggle_todo_status(todo_id: int):
    """Toggle the status of a todo"""
    todo = todo_service.toggle_todo_status(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.get("/todos/status/{status}", response_model=List[TodoItem])
def get_todos_by_status(status: TodoStatus):
    """Get todos by status"""
    return todo_service.get_todos_by_status(status)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)