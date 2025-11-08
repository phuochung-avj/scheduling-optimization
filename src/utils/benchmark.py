# src/utils/benchmark.py
import time
from typing import List
from src.algorithms.base import BaseAlgorithm

class Benchmark:
    """So sánh hiệu suất các thuật toán"""
    
    def compare(self, algorithms: List[BaseAlgorithm]):
        """So sánh các thuật toán"""
        results = []
        
        for algo in algorithms:
            solution = algo.solve()
            results.append({
                'algorithm': solution.algorithm,
                'makespan': solution.makespan,
                'cost': solution.total_cost,
                'execution_time': solution.execution_time,
                'nodes_explored': solution.statistics.get('nodes_explored', 0),
                'backtrack_count': solution.statistics.get('backtrack_count', 0)
            })
        
        return results
    
    def print_comparison(self, results: List[dict]):
        """In bảng so sánh"""
        print("\n" + "="*80)
        print("📊 SO SÁNH CÁC THUẬT TOÁN")
        print("="*80)
        print(f"{'Algorithm':<20} {'Makespan':<12} {'Cost':<12} {'Time(s)':<12} {'Nodes':<12}")
        print("-"*80)
        
        for result in results:
            print(f"{result['algorithm']:<20} {result['makespan']:<12} "
                  f"${result['cost']:<11.2f} {result['execution_time']:<12.4f} "
                  f"{result['nodes_explored']:<12}")
        print("="*80 + "\n")