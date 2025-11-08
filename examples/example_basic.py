# examples/example_basic.py
# examples/example_basic.py
import sys
import os

# Thêm folder gốc vào Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Sau đó mới import
from src.core.models import Task, Resource
from src.core.problem import SchedulingProblem
from src.algorithms.backtracking import BacktrackingScheduler
from src.core.models import Task, Resource

# Tạo bài toán
tasks = [
    Task(id=1, name="Analysis", duration=2, priority=5, 
         resources=['Analyst'], dependencies=[]),
    Task(id=2, name="Design", duration=3, priority=5, 
         resources=['Designer'], dependencies=[1]),
    Task(id=3, name="Development", duration=4, priority=4, 
         resources=['Developer'], dependencies=[2]),
    Task(id=4, name="Testing", duration=3, priority=4, 
         resources=['Tester'], dependencies=[3]),
    Task(id=5, name="Deployment", duration=1, priority=5, 
         resources=['DevOps'], dependencies=[4]),
]

resources = [
    Resource(id='Analyst', name='Business Analyst'),
    Resource(id='Designer', name='UI/UX Designer'),
    Resource(id='Developer', name='Developer'),
    Resource(id='Tester', name='QA Engineer'),
    Resource(id='DevOps', name='DevOps Engineer'),
]

# Tạo problem và solve
problem = SchedulingProblem(tasks, resources, 20)
scheduler = BacktrackingScheduler(problem)

print("⏳ Solving...")
solution = scheduler.solve()

print("\n" + "="*60)
print("📊 KẾT QUẢ")
print("="*60)
print(f"Algorithm: {solution.algorithm}")
print(f"Makespan: {solution.makespan}")
print(f"Total Cost: ${solution.total_cost:.2f}")
print(f"Execution Time: {solution.execution_time:.4f}s")

print("\n📋 LỊCH CHI TIẾT:")
for task_id in sorted(solution.schedule.keys()):
    start = solution.schedule[task_id]
    task = tasks[task_id - 1]
    end = start + task.duration
    print(f"  {task.name}: [{start:2d}-{end:2d}]")

print("\n📈 THỐNG KÊ:")
for key, value in solution.statistics.items():
    print(f"  {key}: {value}")

# In lịch chi tiết
scheduler.print_detailed_schedule()
scheduler.print_statistics()