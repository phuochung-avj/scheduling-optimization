# tests/test_backtracking.py
import pytest
from src.core.problem import SchedulingProblem
from src.algorithms.backtracking import BacktrackingScheduler


def test_football_schedule_basic():
    """Test sắp xếp lịch thi đấu bóng đá cơ bản"""
    problem = SchedulingProblem([], [], 20)
    scheduler = BacktrackingScheduler(problem, num_teams=8, min_rest_days=2)
    solution = scheduler.solve()
    
    assert solution.schedule is not None
    assert len(solution.schedule) == 28  # 28 trận
    assert solution.makespan > 0
    assert solution.algorithm == "Backtracking"
    
    print("✅ test_football_schedule_basic passed")


def test_football_no_team_conflict():
    """Test không có đội nào chơi cùng ngày"""
    problem = SchedulingProblem([], [], 20)
    scheduler = BacktrackingScheduler(problem, num_teams=8, min_rest_days=2)
    solution = scheduler.solve()
    
    # Kiểm tra mỗi ngày không có đội chơi 2 lần
    for day in range(solution.makespan):
        teams_today = set()
        for match_id, scheduled_day in solution.schedule.items():
            if scheduled_day == day:
                match = scheduler.matches[match_id]
                assert match.team1_id not in teams_today, f"Team {match.team1_id} chơi 2 lần ngày {day}"
                assert match.team2_id not in teams_today, f"Team {match.team2_id} chơi 2 lần ngày {day}"
                teams_today.add(match.team1_id)
                teams_today.add(match.team2_id)
    
    print("✅ test_football_no_team_conflict passed")


def test_football_max_matches_per_day():
    """Test mỗi ngày tối đa 2 trận"""
    problem = SchedulingProblem([], [], 20)
    scheduler = BacktrackingScheduler(problem, num_teams=8, min_rest_days=2)
    solution = scheduler.solve()
    
    # Kiểm tra
    for day in range(solution.makespan):
        matches_today = sum(1 for _, d in solution.schedule.items() if d == day)
        assert matches_today <= 2, f"Ngày {day} có {matches_today} trận (max 2)"
    
    print("✅ test_football_max_matches_per_day passed")


def test_football_rest_days():
    """Test mỗi đội có 2 ngày nghỉ giữa các trận"""
    problem = SchedulingProblem([], [], 20)
    scheduler = BacktrackingScheduler(problem, num_teams=8, min_rest_days=2)
    solution = scheduler.solve()
    
    # Kiểm tra rest days
    for team_id in range(8):
        team_play_days = []
        for match_id, day in solution.schedule.items():
            match = scheduler.matches[match_id]
            if team_id in (match.team1_id, match.team2_id):
                team_play_days.append(day)
        
        team_play_days.sort()
        
        # Kiểm tra khoảng cách giữa các ngày thi đấu
        for i in range(len(team_play_days) - 1):
            gap = team_play_days[i + 1] - team_play_days[i]
            assert gap >= 3, f"Team {team_id}: gap={gap} < 3 (ngày {team_play_days[i]} đến {team_play_days[i+1]})"
    
    print("✅ test_football_rest_days passed")


if __name__ == '__main__':
    test_football_schedule_basic()
    test_football_no_team_conflict()
    test_football_max_matches_per_day()
    test_football_rest_days()
    print("\n✅ All football schedule tests passed!")