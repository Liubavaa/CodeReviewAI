import redis
import json


class RedisClient:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def get(self, key: str):
        """
        Retrieve data from Redis.
        """
        cached_data = self.redis.get(key)
        if cached_data:
            return cached_data
        return None

    def set(self, key: str, value: dict):
        """
        Store data in Redis.
        """
        self.redis.set(key, json.dumps(value))

    # def delete(self, key: str):
    #     """
    #     Remove data from Redis.
    #     """
    #     self.redis.delete(key)
