# src/core/models.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Task:
    """Một công việc cần lên lịch"""
    id: int
    name: str
    duration: int  # Thời gian thực hiện
    priority: int = 1  # 1-5, 5 là cao nhất
    resources: List[str] = field(default_factory=list)
    dependencies: List[int] = field(default_factory=list)
    earliest_start: int = 0
    latest_start: Optional[int] = None

@dataclass
class Resource:
    """Một tài nguyên có sẵn"""
    id: str
    name: str
    capacity: int = 1
    cost_per_time_unit: float = 1.0

@dataclass
class Solution:
    """Lời giải cho bài toán scheduling"""
    schedule: Dict[int, int]
    makespan: int
    total_cost: float
    algorithm: str
    execution_time: float
    statistics: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())