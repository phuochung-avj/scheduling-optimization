# src/algorithms/base.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.problem import SchedulingProblem
    from src.core.models import Solution


class BaseAlgorithm(ABC):
    """Base class cho tất cả thuật toán"""
    
    def __init__(self, problem: 'SchedulingProblem'):
        self.problem = problem
        
    @abstractmethod
    def solve(self) -> 'Solution':
        """Giải quyết bài toán - các lớp con phải implement"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Lấy tên thuật toán"""
        pass
    
    def validate_solution(self, solution: 'Solution') -> bool:
        """Kiểm tra solution có hợp lệ không"""
        if not solution.schedule:
            return False
        
        # Kiểm tra tất cả tasks có được lên lịch không
        if len(solution.schedule) != len(self.problem.tasks):
            return False
        
        # Kiểm tra phụ thuộc
        for task_id, start_time in solution.schedule.items():
            task = self.problem.get_task(task_id)
            for dep_id in task.dependencies:
                if dep_id not in solution.schedule:
                    return False
                dep_start = solution.schedule[dep_id]
                dep_task = self.problem.get_task(dep_id)
                dep_end = dep_start + dep_task.duration
                if start_time < dep_end:
                    return False
        
        return True