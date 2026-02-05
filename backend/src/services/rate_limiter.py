import time
from collections import defaultdict, deque
from typing import Dict, Deque
import threading


class RateLimiter:
    """
    Simple rate limiter to prevent abuse of the chat API
    Uses a sliding window approach to track requests per user
    """

    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize the rate limiter

        Args:
            max_requests: Maximum number of requests allowed per window
            window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = threading.Lock()

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a request from the given user is allowed

        Args:
            user_id: The ID of the user making the request

        Returns:
            True if the request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            user_requests = self.requests[user_id]

            # Remove requests that are outside the current window
            while user_requests and current_time - user_requests[0] > self.window_size:
                user_requests.popleft()

            # Check if the user has exceeded the limit
            if len(user_requests) >= self.max_requests:
                return False

            # Add the current request
            user_requests.append(current_time)
            return True


# Global rate limiter instance
chat_rate_limiter = RateLimiter(max_requests=10, window_size=60)  # 10 requests per minute per user