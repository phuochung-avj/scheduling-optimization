
import pytest
from src.core.models import Task, Resource
from src.core.problem import SchedulingProblem
from src.algorithms.backtracking import BacktrackingScheduler

def test_simple_problem():
    """Test bài toán đơn giản"""
    tasks = [
        Task(id=1, name="Task 1", duration=2, priority=1, 
             resources=['R1'], dependencies=[]),
        Task(id=2, name="Task 2", duration=3, priority=1, 
             resources=['R2'], dependencies=[1]),
    ]
    resources = [
        Resource(id='R1', name='Resource 1'),
        Resource(id='R2', name='Resource 2'),
    ]
    
    problem = SchedulingProblem(tasks, resources, 10)
    scheduler = BacktrackingScheduler(problem)
    solution = scheduler.solve()
    
    assert solution.schedule is not None
    assert len(solution.schedule) == 2
    assert solution.makespan > 0
    assert solution.algorithm == "Backtracking"
    print("✅ test_simple_problem passed")

def test_with_dependencies():
    """Test bài toán có phụ thuộc"""
    tasks = [
        Task(id=1, name="Task 1", duration=2, resources=['R1']),
        Task(id=2, name="Task 2", duration=1, resources=['R1'], 
             dependencies=[1]),
        Task(id=3, name="Task 3", duration=2, resources=['R1'], 
             dependencies=[2]),
    ]
    resources = [Resource(id='R1', name='R1')]
    
    problem = SchedulingProblem(tasks, resources, 10)
    scheduler = BacktrackingScheduler(problem)
    solution = scheduler.solve()
    
    # Kiểm tra phụ thuộc
    assert solution.schedule[1] < solution.schedule[2]
    assert solution.schedule[2] < solution.schedule[3]
    print(f"✅ test_with_dependencies passed")

if __name__ == '__main__':
    test_simple_problem()
    test_with_dependencies()
    print("✅ All tests passed!")