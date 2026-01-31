from typing import List, Optional
from models.todo import TodoItem, TodoStatus
import sqlite3
import json
from datetime import datetime


class TodoService:
    def __init__(self, db_path: str = "todo.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with todos table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create todos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()

    def create_todo(self, todo: TodoItem) -> TodoItem:
        """Create a new todo item"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO todos (title, description, status, priority, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (todo.title, todo.description, todo.status.value, todo.priority.value, todo.due_date))
        
        todo.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return todo

    def get_all_todos(self) -> List[TodoItem]:
        """Get all todo items"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, status, priority, created_at, due_date, completed_at
            FROM todos
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        todos = []
        for row in rows:
            todo_data = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": TodoStatus(row[3]),
                "priority": row[4],
                "created_at": datetime.fromisoformat(row[5]) if row[5] else None,
                "due_date": datetime.fromisoformat(row[6]) if row[6] else None,
                "completed_at": datetime.fromisoformat(row[7]) if row[7] else None
            }
            todos.append(TodoItem(**todo_data))
        
        conn.close()
        return todos

    def get_todo_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """Get a specific todo item by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, status, priority, created_at, due_date, completed_at
            FROM todos
            WHERE id = ?
        """, (todo_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            todo_data = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": TodoStatus(row[3]),
                "priority": row[4],
                "created_at": datetime.fromisoformat(row[5]) if row[5] else None,
                "due_date": datetime.fromisoformat(row[6]) if row[6] else None,
                "completed_at": datetime.fromisoformat(row[7]) if row[7] else None
            }
            return TodoItem(**todo_data)
        
        return None

    def update_todo(self, todo_id: int, todo: TodoItem) -> Optional[TodoItem]:
        """Update a todo item"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE todos
            SET title = ?, description = ?, status = ?, priority = ?, due_date = ?
            WHERE id = ?
        """, (todo.title, todo.description, todo.status.value, todo.priority.value, todo.due_date, todo_id))
        
        conn.commit()
        conn.close()
        
        return self.get_todo_by_id(todo_id)

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted

    def toggle_todo_status(self, todo_id: int) -> Optional[TodoItem]:
        """Toggle the status of a todo item"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            if todo.status == TodoStatus.COMPLETED:
                todo.status = TodoStatus.PENDING
                todo.completed_at = None
            else:
                todo.status = TodoStatus.COMPLETED
                todo.completed_at = datetime.now()
            
            return self.update_todo(todo_id, todo)
        
        return None

    def get_todos_by_status(self, status: TodoStatus) -> List[TodoItem]:
        """Get todos filtered by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, status, priority, created_at, due_date, completed_at
            FROM todos
            WHERE status = ?
            ORDER BY created_at DESC
        """, (status.value,))
        
        rows = cursor.fetchall()
        todos = []
        for row in rows:
            todo_data = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": TodoStatus(row[3]),
                "priority": row[4],
                "created_at": datetime.fromisoformat(row[5]) if row[5] else None,
                "due_date": datetime.fromisoformat(row[6]) if row[6] else None,
                "completed_at": datetime.fromisoformat(row[7]) if row[7] else None
            }
            todos.append(TodoItem(**todo_data))
        
        conn.close()
        return todos