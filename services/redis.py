import redis
from app.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)

redis_client.setex(f"user:{user.id}", 300, user.email)
