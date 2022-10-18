from fastapi_redis_cache import FastApiRedisCache

import os

LOCAL_REDIS_URL = "redis://localhost:6379" if os.environ.get("SO") is None else "redis://redis:6379"


# https://pypi.org/project/fastapi-redis-cache/