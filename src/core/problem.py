# src/core/problem.py
from typing import List
from src.core.models import Task, Resource

class SchedulingProblem:
    """Đại diện cho bài toán scheduling"""
    
    def __init__(self, tasks: List[Task], resources: List[Resource], time_horizon: int):
        self.tasks = {t.id: t for t in tasks}
        self.resources = {r.id: r for r in resources}
        self.time_horizon = time_horizon
        self.task_list = list(tasks)
        
    def validate(self) -> bool:
        """Kiểm tra bài toán hợp lệ"""
        if not self.tasks:
            return False
        if not self.resources:
            return False
        if self.time_horizon <= 0:
            return False
        
        # Kiểm tra dependencies tồn tại
        for task in self.task_list:
            for dep_id in task.dependencies:
                if dep_id not in self.tasks:
                    return False
        
        return True
    
    def get_task(self, task_id: int) -> Task:
        return self.tasks.get(task_id)
    
    def get_resource(self, res_id: str) -> Resource:
        return self.resources.get(res_id)