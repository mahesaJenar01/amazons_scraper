from typing import List, Set
from datetime import datetime
from collections import deque
from dataclasses import dataclass

@dataclass
class RetryItem:
    url: str
    attempts: int = 0
    last_attempt: datetime = None

class RetryManager:
    def __init__(self, max_attempts: int = 2):
        self.retry_queue = deque()
        self.failed_urls: Set[str] = set()
        self.max_attempts = max_attempts
        
    def add_retry(self, url: str):
        if url not in self.failed_urls:
            self.retry_queue.append(RetryItem(url))
            self.failed_urls.add(url)
            
    def get_next_retry(self) -> RetryItem:
        return self.retry_queue.popleft() if self.retry_queue else None
        
    def should_retry(self, url: str) -> bool:
        return url in self.failed_urls