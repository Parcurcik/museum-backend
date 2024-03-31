import redis


class RedisTools:

    __redis_connect = redis.Redis(host='redis', port=6379)
