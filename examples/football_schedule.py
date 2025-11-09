import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.problem import SchedulingProblem
from src.algorithms.backtracking import BacktrackingScheduler


def main():
    print("\n" + "="*80)
    print("⚽ CHƯƠNG TRÌNH SẮP XẾP LỊCH THI ĐẤU BÓNG ĐÁ NGOẠI HẠNG ANH")
    print("="*80)
    print("\n📋 Thông tin bài toán:")
    print("  • Số đội: 8")
    print("  • Hình thức: Vòng tròn (mỗi đội thi với mỗi đội khác 1 lần)")
    print("  • Tổng trận: 28 trận")
    print("  • Ràng buộc 1: Mỗi ngày tối đa 2 trận")
    print("  • Ràng buộc 2: Mỗi đội có 2 ngày nghỉ giữa các trận")
    print("  • Thuật toán: Backtracking")
    
    # Định nghĩa tên các đội
    team_names = {
        0: "Manchester United",
        1: "Liverpool",
        2: "Manchester City",
        3: "Chelsea",
        4: "Arsenal",
        5: "Tottenham",
        6: "Newcastle",
        7: "Brighton"
    }
    
    problem = SchedulingProblem([], [], 20)
    
    # Tạo scheduler với tên đội
    scheduler = BacktrackingScheduler(
        problem, 
        num_teams=8, 
        min_rest_days=2,
        team_names=team_names
    )
    
    print("\n⏳ Đang sắp xếp lịch...")
    solution = scheduler.solve()
    
    if solution.schedule:
        print(f"\n✅ Tìm được lịch thi đấu!")
        print(f"   Thời gian: {solution.execution_time:.4f} giây")
        
        scheduler.print_schedule()
        scheduler.print_statistics()
        
        print("\n" + "="*80)
        print("📊 TÓM TẮT KẾT QUẢ")
        print("="*80)
        print(f"✓ Tổng số ngày: {solution.makespan}")
        print(f"✓ Tổng số trận: {len(solution.schedule)}")
        print(f"✓ Trung bình trận/ngày: {len(solution.schedule) / solution.makespan:.2f}")
        print(f"✓ Thời gian tìm kiếm: {solution.execution_time:.4f} giây")
        print("="*80 + "\n")
    else:
        print("\n❌ Không tìm được lịch thi đấu!")


if __name__ == '__main__':
    main()