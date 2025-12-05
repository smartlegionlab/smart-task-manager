# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import json
import os
from typing import Dict, Optional

from core.task import Task


class TaskManager:

    def __init__(self, filename: str = '~/.todos.json'):
        self.filename = os.path.expanduser(filename)
        self.tasks = self._load_data()

    @property
    def count(self) -> int:
        return len(self.tasks)

    @property
    def completed_count(self) -> int:
        return sum(1 for task in self.tasks.values() if task.completed)

    def add_task(self, task: Task):
        self.tasks[task.id] = task
        self._write_data()

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._write_data()
        else:
            raise KeyError("Task not found.")

    def clear_completed(self):
        completed_ids = [task_id for task_id, task in self.tasks.items() if task.completed]
        for task_id in completed_ids:
            del self.tasks[task_id]
        if completed_ids:
            self._write_data()

    def clear_all(self):
        self.tasks = {}
        self._write_data()

    def get_tasks_by_priority(self) -> Dict[int, list]:
        grouped = {1: [], 2: [], 3: []}
        for task in self.tasks.values():
            grouped[task.priority].append(task)
        return grouped

    def _load_data(self) -> Dict[str, Task]:
        if os.path.isfile(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return {task_id: Task.from_dict(task_data)
                            for task_id, task_data in data.items()}
            except (json.JSONDecodeError, IOError):
                return {}
        else:
            return {}

    def _write_data(self):
        with open(self.filename, 'w') as f:
            json.dump({task_id: task.to_dict()
                       for task_id, task in self.tasks.items()}, f, indent=4)
