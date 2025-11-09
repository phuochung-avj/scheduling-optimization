"""
Sắp xếp lịch thi đấu bóng đá - Backtracking Algorithm
File: src/algorithms/backtracking.py

Bài toán:
- 8 đội bóng
- Thi đấu vòng tròn (mỗi đội thi với mỗi đội khác 1 lần)
- Mỗi ngày tối đa 2 trận
- Mỗi đội có tối thiểu 2 ngày nghỉ giữa các trận
"""

import time
import logging
from typing import Dict, List, Optional
from src.algorithms.base import BaseAlgorithm
from src.core.models import Solution
from src.core.problem import SchedulingProblem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FootballMatch:
    """Đại diện cho một trận đấu"""
    def __init__(self, match_id: int, team1_id: int, team2_id: int, 
                 team1_name: str = "", team2_name: str = ""):
        self.match_id = match_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.team1_name = team1_name
        self.team2_name = team2_name
    
    def __repr__(self):
        if self.team1_name and self.team2_name:
            return f"Match({self.team1_name} vs {self.team2_name})"
        return f"Match({self.team1_id} vs {self.team2_id})"


class BacktrackingScheduler(BaseAlgorithm):
    """
    Sắp xếp lịch thi đấu bóng đá bằng Backtracking
    
    Ràng buộc:
    1. Mỗi ngày tối đa 2 trận
    2. Mỗi đội có tối thiểu 2 ngày nghỉ giữa các trận
    3. Mỗi đội thi đấu với mỗi đội khác đúng 1 lần
    """
    
    def __init__(self, problem: SchedulingProblem, num_teams: int = 8, 
                 min_rest_days: int = 2, team_names: Dict[int, str] = None):
        super().__init__(problem)
        self.num_teams = num_teams
        self.min_rest_days = min_rest_days
        
        # Danh sách tên đội
        if team_names is None:
            self.team_names = {i: f"Đội {i}" for i in range(num_teams)}
        else:
            self.team_names = team_names
        
        # Tạo danh sách tất cả các trận đấu
        self.matches = self._generate_matches()
        self.total_matches = len(self.matches)
        
        # Lịch: match_id -> day (ngày thi đấu)
        self.schedule = {}
        
        # Lịch sử thi đấu của mỗi đội: team_id -> [day1, day2, ...]
        self.team_play_days = {i: [] for i in range(num_teams)}
        
        # Số trận tối đa mỗi ngày
        self.max_matches_per_day = 2
        
        # Số ngày cần thiết: tối thiểu là ceil(total_matches / 2)
        self.num_days_needed = (self.total_matches + self.max_matches_per_day - 1) // self.max_matches_per_day
        
        self.stats = {
            'nodes_explored': 0,
            'backtrack_count': 0,
            'solutions_found': 0
        }
        
        logger.info(f"✓ Initialized Football Scheduler: {num_teams} teams, "
                   f"{self.total_matches} matches, min {self.num_days_needed} days needed")
    
    def _generate_matches(self) -> List[FootballMatch]:
        """
        Tạo tất cả các trận đấu (vòng tròn)
        Mỗi đội thi đấu với mỗi đội khác đúng 1 lần
        """
        matches = []
        match_id = 0
        
        for team1_id in range(self.num_teams):
            for team2_id in range(team1_id + 1, self.num_teams):
                team1_name = self.team_names[team1_id]
                team2_name = self.team_names[team2_id]
                
                matches.append(FootballMatch(
                    match_id, team1_id, team2_id, 
                    team1_name, team2_name
                ))
                match_id += 1
        
        return matches
    
    def get_name(self) -> str:
        return "Backtracking"
    
    def solve(self) -> Solution:
        """Giải bài toán sắp xếp lịch thi đấu"""
        start_time = time.time()
        
        # Reset
        self.schedule = {}
        self.team_play_days = {i: [] for i in range(self.num_teams)}
        self.stats = {
            'nodes_explored': 0,
            'backtrack_count': 0,
            'solutions_found': 0
        }
        
        logger.info("🔍 Bắt đầu sắp xếp lịch thi đấu...")
        
        # Chạy backtracking
        self._backtrack(0, 0)  # match_idx=0, day=0
        
        execution_time = time.time() - start_time
        
        # Tạo Solution
        if self.schedule:
            makespan = max(self.schedule.values()) + 1 if self.schedule else 0
            
            # Tính chi phí (không cần cho bài này, nhưng giữ format)
            total_cost = 0.0
            
            solution = Solution(
                schedule=self.schedule.copy(),
                makespan=makespan,
                total_cost=total_cost,
                algorithm=self.get_name(),
                execution_time=execution_time,
                statistics=self.stats
            )
            
            logger.info(f"✓ Tìm được lịch thi đấu: {makespan} ngày")
            return solution
        
        logger.warning("❌ Không tìm được lịch thi đấu")
        return Solution(
            schedule={},
            makespan=0,
            total_cost=0,
            algorithm=self.get_name(),
            execution_time=execution_time,
            statistics=self.stats
        )
    
    def _is_valid_placement(self, match_idx: int, day: int) -> bool:
        """
        Kiểm tra xem có thể đặt trận đấu tại ngày này không
        
        Kiểm tra:
        1. Số trận trong ngày không vượt 2
        2. Mỗi đội có ít nhất 2 ngày nghỉ giữa các trận
        """
        match = self.matches[match_idx]
        team1 = match.team1_id
        team2 = match.team2_id
        
        # Kiểm tra số trận tối đa trong ngày
        matches_today = sum(1 for m_id, d in self.schedule.items() if d == day)
        if matches_today >= self.max_matches_per_day:
            return False
        
        # Kiểm tra hai đội không cùng thi đấu cùng ngày
        for m_id, d in self.schedule.items():
            if d == day:
                m = self.matches[m_id]
                if team1 in (m.team1_id, m.team2_id) or team2 in (m.team1_id, m.team2_id):
                    return False
        
        # Kiểm tra rest days cho team1
        if self.team_play_days[team1]:
            last_play_day = max(self.team_play_days[team1])
            if day - last_play_day < self.min_rest_days + 1:
                return False
        
        # Kiểm tra rest days cho team2
        if self.team_play_days[team2]:
            last_play_day = max(self.team_play_days[team2])
            if day - last_play_day < self.min_rest_days + 1:
                return False
        
        return True
    
    def _place_match(self, match_idx: int, day: int):
        """Đặt trận đấu vào lịch"""
        match = self.matches[match_idx]
        self.schedule[match_idx] = day
        
        # Cập nhật ngày thi đấu của mỗi đội
        if day not in self.team_play_days[match.team1_id]:
            self.team_play_days[match.team1_id].append(day)
        if day not in self.team_play_days[match.team2_id]:
            self.team_play_days[match.team2_id].append(day)
    
    def _remove_match(self, match_idx: int):
        """Gỡ trận đấu khỏi lịch"""
        if match_idx not in self.schedule:
            return
        
        match = self.matches[match_idx]
        day = self.schedule[match_idx]
        del self.schedule[match_idx]
        
        # Cập nhật team play days
        self.team_play_days[match.team1_id] = [d for d in self.team_play_days[match.team1_id]
                                                if d in [self.schedule.get(m_id) for m_id in self.schedule]]
        self.team_play_days[match.team2_id] = [d for d in self.team_play_days[match.team2_id]
                                                if d in [self.schedule.get(m_id) for m_id in self.schedule]]
        
        self.stats['backtrack_count'] += 1
    
    def _backtrack(self, match_idx: int, current_day: int) -> bool:
        """
        Thuật toán backtracking chính
        
        Args:
            match_idx: Chỉ số trận đấu cần sắp xếp
            current_day: Ngày hiện tại
        """
        self.stats['nodes_explored'] += 1
        
        # Base case: tất cả trận đấu đã được sắp xếp
        if match_idx == self.total_matches:
            self.stats['solutions_found'] += 1
            logger.info(f"✓ Lịch thi đấu #{self.stats['solutions_found']} tìm được!")
            return True
        
        # Thử từng ngày bắt đầu từ current_day
        for day in range(current_day, current_day + 20):  # Giới hạn tìm kiếm
            if self._is_valid_placement(match_idx, day):
                # Đặt trận
                self._place_match(match_idx, day)
                
                # Tiếp tục backtrack
                next_day = max(current_day, day)
                if self._backtrack(match_idx + 1, next_day):
                    return True
                
                # Backtrack
                self._remove_match(match_idx)
        
        return False
    
    def print_schedule(self, schedule: Dict[int, int] = None):
        """In lịch thi đấu"""
        if schedule is None:
            schedule = self.schedule
        
        if not schedule:
            logger.warning("Không có lịch để hiển thị")
            return
        
        print("\n" + "="*80)
        print("⚽ LỊCH THI ĐẤU BÓNG ĐÁ - VÒNG TRÒN")
        print("="*80)
        
        # Sắp xếp theo ngày
        days_matches = {}
        for match_id, day in sorted(schedule.items(), key=lambda x: x[1]):
            if day not in days_matches:
                days_matches[day] = []
            days_matches[day].append(match_id)
        
        # In theo ngày
        for day in sorted(days_matches.keys()):
            print(f"\n📅 NGÀY {day + 1}:")
            print("-" * 80)
            for match_id in days_matches[day]:
                match = self.matches[match_id]
                print(f"  Trận {match_id + 1}: {match.team1_name} vs {match.team2_name}")
        
        # Thống kê
        total_days = max(schedule.values()) + 1 if schedule else 0
        
        print("\n" + "="*80)
        print("📊 THỐNG KÊ")
        print("="*80)
        print(f"Tổng số trận: {len(schedule)}")
        print(f"Tổng số ngày: {total_days}")
        print(f"Trận/ngày: {len(schedule) / total_days:.1f} (Tối đa: {self.max_matches_per_day})")
        
        # In lịch thi đấu theo đội
        print("\n" + "-"*80)
        print("📋 LỊCH THAM DỰ CỦA MỖI ĐỘI")
        print("-"*80)
        
        for team_id in range(self.num_teams):
            matches = [(match_id, schedule[match_id]) 
                      for match_id in schedule 
                      if team_id in (self.matches[match_id].team1_id, self.matches[match_id].team2_id)]
            
            matches.sort(key=lambda x: x[1])
            
            team_name = self.team_names[team_id]
            print(f"\n🏆 {team_name}:")
            for match_id, day in matches:
                match = self.matches[match_id]
                opponent_id = match.team2_id if match.team1_id == team_id else match.team1_id
                opponent_name = self.team_names[opponent_id]
                print(f"  Ngày {day + 1}: vs {opponent_name}")
        
        print("\n" + "="*80 + "\n")
    
    def print_statistics(self):
        """In thống kê"""
        print("\n" + "="*80)
        print("📈 THỐNG KÊ BACKTRACKING")
        print("="*80)
        print(f"Nodes explored: {self.stats['nodes_explored']}")
        print(f"Backtrack count: {self.stats['backtrack_count']}")
        print(f"Solutions found: {self.stats['solutions_found']}")
        print("="*80 + "\n")