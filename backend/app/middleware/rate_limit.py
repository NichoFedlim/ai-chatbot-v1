"""
Rate limiting middleware for API endpoints.
"""
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import threading

from fastapi import HTTPException, Request
from ..config import settings

class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, key: str) -> Tuple[bool, int]:
        """Check if request is allowed for given key."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        with self.lock:
            # Clean old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key] 
                if req_time > window_start
            ]
            
            # Check if under limit
            if len(self.requests[key]) < self.max_requests:
                self.requests[key].append(now)
                remaining = self.max_requests - len(self.requests[key])
                return True, remaining
            else:
                remaining = 0
                return False, remaining

# Create rate limiter instance
rate_limiter = RateLimiter(settings.rate_limit_per_minute)

def rate_limit():
    """Decorator for rate limiting."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request object
            request = next(
                (arg for arg in args if isinstance(arg, Request)),
                None
            )
            
            if not request:
                # Try to find request in kwargs
                request = kwargs.get('request')
            
            if request:
                # Use client IP as key
                client_ip = request.client.host if request.client else "unknown"
                key = f"{client_ip}:{request.url.path}"
                
                allowed, remaining = rate_limiter.is_allowed(key)
                
                if not allowed:
                    raise HTTPException(
                        status_code=429,
                        detail="Rate limit exceeded. Please try again later.",
                        headers={"X-RateLimit-Limit": str(settings.rate_limit_per_minute)}
                    )
                
                # Add rate limit headers to response
                response = await func(*args, **kwargs)
                response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                return response
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator