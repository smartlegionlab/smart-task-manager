# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from datetime import datetime
from typing import Dict, Optional


class Task:

    def __init__(self, id: str, title: str, description: str = "",
                 priority: int = 3, completed: bool = False,
                 created_at: Optional[str] = None, due_date: Optional[str] = None):
        self._id = id
        self._title = title
        self._description = description
        self._priority = priority
        self._completed = completed
        self._created_at = created_at or datetime.now().isoformat()
        self._due_date = due_date

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def due_date(self) -> Optional[str]:
        return self._due_date

    def toggle_complete(self):
        self._completed = not self._completed

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "priority": self._priority,
            "completed": self._completed,
            "created_at": self._created_at,
            "due_date": self._due_date
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        return Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            completed=data['completed'],
            created_at=data['created_at'],
            due_date=data.get('due_date')
        )
