"""
Giải bài toán sắp xếp lịch (Scheduling) bằng Backtracking - Version đơn giản
File: src/algorithms/backtracking.py
"""

import time
import logging
from typing import Dict, Optional, List
from src.algorithms.base import BaseAlgorithm
from src.core.models import Solution
from src.core.problem import SchedulingProblem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BacktrackingScheduler(BaseAlgorithm):
    """
    Giải bài toán scheduling bằng Backtracking
    
    Thuật toán:
    - Thử đặt từng công việc vào từng thời gian
    - Kiểm tra ràng buộc (dependencies, resources)
    - Backtrack khi gặp xung đột
    """
    
    def __init__(self, problem: SchedulingProblem):
        super().__init__(problem)
        self.schedule = {}
        self.resource_usage = {}
        self.stats = {
            'nodes_explored': 0,
            'backtrack_count': 0,
            'solutions_found': 0
        }
        
        # Khởi tạo resource usage tracking
        for res_id in self.problem.resources:
            self.resource_usage[res_id] = [False] * problem.time_horizon
    
    def get_name(self) -> str:
        return "Backtracking"
    
    def solve(self) -> Solution:
        """Giải bài toán scheduling"""
        start_time = time.time()
        
        # Reset
        self.schedule = {}
        self.stats = {
            'nodes_explored': 0,
            'backtrack_count': 0,
            'solutions_found': 0
        }
        for res_id in self.problem.resources:
            self.resource_usage[res_id] = [False] * self.problem.time_horizon
        
        logger.info("🔍 Bắt đầu tìm kiếm...")
        
        # Gọi backtrack
        self._backtrack(list(self.problem.tasks.keys()), 0)
        
        execution_time = time.time() - start_time
        
        # Tạo Solution
        if self.schedule:
            makespan = self._calculate_makespan(self.schedule)
            total_cost = self._calculate_cost(self.schedule)
            
            solution = Solution(
                schedule=self.schedule.copy(),
                makespan=makespan,
                total_cost=total_cost,
                algorithm=self.get_name(),
                execution_time=execution_time,
                statistics=self.stats
            )
            
            if self.validate_solution(solution):
                logger.info(f"✓ Tìm được lời giải: makespan={makespan}")
                return solution
        
        logger.warning("❌ Không tìm được lời giải")
        return Solution(
            schedule={},
            makespan=0,
            total_cost=0,
            algorithm=self.get_name(),
            execution_time=execution_time,
            statistics=self.stats
        )
    
    def _can_place_task(self, task_id: int, start_time: int) -> bool:
        """
        Kiểm tra có thể đặt công việc tại thời gian này không
        
        Kiểm tra:
        1. Thời gian không vượt quá time_horizon
        2. Tất cả dependencies đã được schedule
        3. Dependencies hoàn thành trước task này
        4. Tài nguyên có sẵn
        """
        task = self.problem.tasks[task_id]
        end_time = start_time + task.duration
        
        # Kiểm tra time bound
        if start_time < 0 or end_time > self.problem.time_horizon:
            return False
        
        # Kiểm tra dependencies
        for dep_id in task.dependencies:
            # Dependency phải được schedule rồi
            if dep_id not in self.schedule:
                return False
            
            # Dependency phải hoàn thành trước khi task này bắt đầu
            dep_end = self.schedule[dep_id] + self.problem.tasks[dep_id].duration
            if start_time < dep_end:
                return False
        
        # Kiểm tra tài nguyên
        for res_id in task.resources:
            for t in range(start_time, end_time):
                if self.resource_usage[res_id][t]:
                    return False
        
        return True
    
    def _place_task(self, task_id: int, start_time: int):
        """Đặt công việc vào lịch"""
        task = self.problem.tasks[task_id]
        self.schedule[task_id] = start_time
        
        for res_id in task.resources:
            for t in range(start_time, start_time + task.duration):
                self.resource_usage[res_id][t] = True
    
    def _remove_task(self, task_id: int):
        """Gỡ công việc khỏi lịch"""
        if task_id not in self.schedule:
            return
        
        task = self.problem.tasks[task_id]
        start_time = self.schedule[task_id]
        del self.schedule[task_id]
        
        for res_id in task.resources:
            for t in range(start_time, start_time + task.duration):
                self.resource_usage[res_id][t] = False
        
        self.stats['backtrack_count'] += 1
    
    def _backtrack(self, remaining_tasks: List[int], depth: int) -> bool:
        """
        Thuật toán backtrack chính
        
        Args:
            remaining_tasks: Danh sách công việc chưa schedule
            depth: Độ sâu recursion
            
        Returns:
            True nếu tìm được lời giải
        """
        self.stats['nodes_explored'] += 1
        
        # Base case: tất cả công việc đã schedule
        if not remaining_tasks:
            self.stats['solutions_found'] += 1
            logger.info(f"✓ Lời giải #{self.stats['solutions_found']} tìm được")
            return True
        
        # Chọn công việc tiếp theo (công việc đầu tiên)
        task_id = remaining_tasks[0]
        new_remaining = remaining_tasks[1:]
        
        # Thử từng thời gian bắt đầu
        for start_time in range(self.problem.time_horizon):
            if self._can_place_task(task_id, start_time):
                # Đặt công việc
                self._place_task(task_id, start_time)
                
                # Tiếp tục backtrack
                if self._backtrack(new_remaining, depth + 1):
                    return True  # Tìm được lời giải, return ngay
                
                # Backtrack - gỡ công việc
                self._remove_task(task_id)
        
        return False
    
    def _calculate_makespan(self, schedule: Dict[int, int]) -> int:
        """Tính makespan (thời gian hoàn thành)"""
        if not schedule:
            return 0
        return max(schedule[t_id] + self.problem.tasks[t_id].duration 
                  for t_id in schedule)
    
    def _calculate_cost(self, schedule: Dict[int, int]) -> float:
        """Tính tổng chi phí"""
        cost = 0
        for task_id, start_time in schedule.items():
            task = self.problem.tasks[task_id]
            for res_id in task.resources:
                res = self.problem.resources[res_id]
                cost += res.cost_per_time_unit * task.duration
        return cost
    
    def print_detailed_schedule(self, schedule: Dict[int, int] = None):
        """In lịch sắp xếp chi tiết"""
        if schedule is None:
            schedule = self.schedule
        
        if not schedule:
            logger.warning("Không có lịch để hiển thị")
            return
        
        print("\n" + "="*80)
        print("📊 LỊCH SẮP XẾP CHI TIẾT")
        print("="*80)
        print(f"{'Task ID':<8} {'Task Name':<20} {'Time':<12} {'Duration':<10} {'Resources':<20}")
        print("-"*80)
        
        for task_id in sorted(schedule.keys()):
            task = self.problem.tasks[task_id]
            start = schedule[task_id]
            end = start + task.duration
            time_slot = f"[{start:2d}-{end:2d}]"
            resources_str = ", ".join(task.resources) if task.resources else "None"
            
            print(f"{task_id:<8} {task.name:<20} {time_slot:<12} {task.duration:<10} {resources_str:<20}")
        
        # In resource timeline
        print("\n" + "-"*80)
        print("📈 TIMELINE TÀI NGUYÊN")
        print("-"*80)
        
        for res_id in sorted(self.resource_usage.keys()):
            res = self.problem.resources[res_id]
            print(f"\n{res.name}: ", end="")
            for t in range(self.problem.time_horizon):
                if self.resource_usage[res_id][t]:
                    print("█", end="")
                else:
                    print("_", end="")
            
            used = sum(1 for x in self.resource_usage[res_id] if x)
            utilization = used / self.problem.time_horizon * 100
            print(f" {utilization:.1f}%")
        
        # Tóm tắt
        makespan = self._calculate_makespan(schedule)
        total_cost = self._calculate_cost(schedule)
        
        print("\n" + "="*80)
        print(f"⏱️  Makespan: {makespan}")
        print(f"💰 Chi phí: ${total_cost:.2f}")
        print(f"📊 Công việc: {len(schedule)}/{len(self.problem.tasks)}")
        print("="*80 + "\n")
    
    def print_statistics(self):
        """In thống kê"""
        print("\n" + "="*80)
        print("📈 THỐNG KÊ BACKTRACKING")
        print("="*80)
        print(f"Nodes explored: {self.stats['nodes_explored']}")
        print(f"Backtrack count: {self.stats['backtrack_count']}")
        print(f"Solutions found: {self.stats['solutions_found']}")
        print("="*80 + "\n")