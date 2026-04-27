import time
import random
import asyncio
from typing import Optional
import httpx

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
]


def get_random_headers() -> dict:
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


class RateLimiter:
    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay

    async def wait(self):
        delay = random.uniform(self.min_delay, self.max_delay)
        await asyncio.sleep(delay)


async def async_fetch(
    url: str,
    headers: Optional[dict] = None,
    proxy: Optional[str] = None,
    retry_count: int = 3,
    rate_limiter: Optional[RateLimiter] = None,
) -> httpx.Response:
    client_headers = headers or get_random_headers()

    async with httpx.AsyncClient(
        timeout=30.0,
        proxy=proxy,
        follow_redirects=True,
    ) as client:
        for attempt in range(retry_count):
            try:
                response = await client.get(url, headers=client_headers)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                if attempt == retry_count - 1:
                    raise
                wait_time = min(2**attempt * 2, 30)
                await asyncio.sleep(wait_time)

    raise RuntimeError(f"Failed to fetch {url} after {retry_count} retries")
