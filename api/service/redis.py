import redis.asyncio as redis
from api.configuration.config import settings


class RedisService:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

    async def set_code(self, phone_number: str, code: str, expire: int = 600) -> None:
        """Сохранение кода в Redis с истечением срока действия (expire в секундах)"""
        await self.redis.setex(phone_number, expire, code)

    async def get_code(self, phone_number: str) -> str:
        """Получение кода из Redis"""
        return await self.redis.get(phone_number)

    async def delete_code(self, phone_number: str) -> None:
        """Удаление кода из Redis"""
        await self.redis.delete(phone_number)


redis_service = RedisService()
