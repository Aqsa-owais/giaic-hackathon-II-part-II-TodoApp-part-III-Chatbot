"""
Simple monitoring and metrics collection for the AI Agent & Chat API
"""
import time
import threading
from collections import defaultdict, deque
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class RequestMetrics:
    """Data class to hold request metrics"""
    request_id: str
    user_id: str
    timestamp: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    conversation_id: Optional[str] = None


class MetricsCollector:
    """
    Simple metrics collector to track agent performance and usage
    """

    def __init__(self, retention_hours: int = 24):
        self.retention_seconds = retention_hours * 3600
        self.metrics: List[RequestMetrics] = []
        self.lock = threading.Lock()

        # Counters
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        # Performance tracking
        self.total_duration = 0.0

    def record_request(self, request_id: str, user_id: str, duration: float,
                      success: bool, error_message: Optional[str] = None,
                      conversation_id: Optional[str] = None):
        """Record a request metric"""
        with self.lock:
            metric = RequestMetrics(
                request_id=request_id,
                user_id=user_id,
                timestamp=time.time(),
                duration=duration,
                success=success,
                error_message=error_message,
                conversation_id=conversation_id
            )

            self.metrics.append(metric)
            self.total_requests += 1

            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

            self.total_duration += duration

            # Clean old metrics
            self._cleanup_old_metrics()

    def _cleanup_old_metrics(self):
        """Remove metrics older than retention period"""
        cutoff_time = time.time() - self.retention_seconds
        with self.lock:
            self.metrics = [m for m in self.metrics if m.timestamp > cutoff_time]

    def get_request_count(self, hours: int = 1) -> int:
        """Get request count for the last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        with self.lock:
            return len([m for m in self.metrics if m.timestamp > cutoff_time])

    def get_success_rate(self) -> float:
        """Get overall success rate"""
        with self.lock:
            if self.total_requests == 0:
                return 0.0
            return (self.successful_requests / self.total_requests) * 100

    def get_average_response_time(self) -> float:
        """Get average response time"""
        with self.lock:
            if self.total_requests == 0:
                return 0.0
            return self.total_duration / self.total_requests

    def get_error_rate(self) -> float:
        """Get error rate"""
        with self.lock:
            if self.total_requests == 0:
                return 0.0
            return (self.failed_requests / self.total_requests) * 100

    def get_top_errors(self, limit: int = 5) -> Dict[str, int]:
        """Get top errors by frequency"""
        error_counts = defaultdict(int)
        with self.lock:
            for metric in self.metrics:
                if not metric.success and metric.error_message:
                    error_counts[metric.error_message] += 1

        # Sort by count and return top N
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_errors[:limit])


# Global metrics collector instance
metrics_collector = MetricsCollector(retention_hours=24)