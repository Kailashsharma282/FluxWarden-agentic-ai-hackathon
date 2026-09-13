import json
import logging
import time
from typing import Any, Optional, Callable, Coroutine
from app.config import settings

logger = logging.getLogger("fluxwarden.redis")

class RedisManager:
    """
    Section 44: Redis Coordinator for live agent state, WebSocket coordination,
    event streaming, transient locks, and caching.
    Includes in-memory fallback for zero-dependency standalone execution.
    """
    def __init__(self):
        self.redis_client = None
        self._in_memory_cache: dict[str, str] = {}
        self._in_memory_subscribers: list[Callable[[str], Coroutine[Any, Any, None]]] = []
        self._in_memory_locks: dict[str, float] = {}
        self._init_connection()

    def _init_connection(self):
        try:
            import redis.asyncio as aioredis
            self.redis_client = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=2.0
            )
            logger.info(f"Connected to Redis at {settings.REDIS_URL}")
        except Exception as e:
            logger.warning(f"Redis unavailable, operating with in-memory coordination: {e}")
            self.redis_client = None

    async def set_state(self, key: str, value: Any, ttl_seconds: int = 3600):
        val_str = json.dumps(value)
        if self.redis_client:
            try:
                await self.redis_client.set(key, val_str, ex=ttl_seconds)
                return
            except Exception as e:
                logger.debug(f"Redis set failed, disabling redis client: {e}")
                self.redis_client = None
        self._in_memory_cache[key] = val_str

    async def get_state(self, key: str) -> Optional[Any]:
        if self.redis_client:
            try:
                val = await self.redis_client.get(key)
                if val:
                    return json.loads(val)
            except Exception as e:
                logger.debug(f"Redis get failed, disabling redis client: {e}")
                self.redis_client = None
        val = self._in_memory_cache.get(key)
        return json.loads(val) if val else None

    async def publish_event(self, channel: str, event_data: dict[str, Any]):
        payload = json.dumps(event_data)
        if self.redis_client:
            try:
                await self.redis_client.publish(channel, payload)
            except Exception as e:
                logger.debug(f"Redis publish failed, disabling redis client: {e}")
                self.redis_client = None
        # Dispatch to local in-memory subscribers
        for sub in list(self._in_memory_subscribers):
            try:
                await sub(payload)
            except Exception:
                pass

    def subscribe_in_memory(self, callback: Callable[[str], Coroutine[Any, Any, None]]):
        if callback not in self._in_memory_subscribers:
            self._in_memory_subscribers.append(callback)

    async def acquire_lock(self, lock_name: str, timeout_seconds: int = 10) -> bool:
        if self.redis_client:
            try:
                acquired = await self.redis_client.set(f"lock:{lock_name}", "1", nx=True, ex=timeout_seconds)
                return bool(acquired)
            except Exception:
                self.redis_client = None
                pass
        # In-memory lock fallback
        now = time.time()
        expiry = self._in_memory_locks.get(lock_name, 0)
        if now > expiry:
            self._in_memory_locks[lock_name] = now + timeout_seconds
            return True
        return False

    async def release_lock(self, lock_name: str):
        if self.redis_client:
            try:
                await self.redis_client.delete(f"lock:{lock_name}")
            except Exception:
                pass
        self._in_memory_locks.pop(lock_name, None)

redis_manager = RedisManager()
