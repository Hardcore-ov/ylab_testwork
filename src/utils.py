import json
import uuid

from fastapi.encoders import jsonable_encoder

from src.database import redis


def generate_uuid():
    return str(uuid.uuid4())


def generate_key(prefix, body):
    key = f'{prefix}:{body}'
    return key


async def get_cache(prefix, body):
    key = generate_key(prefix, body)
    value = await redis.get(key)
    return json.loads(value) if value else None


async def set_cache(prefix, body, value):
    key = generate_key(prefix, body)
    await redis.set(key, json.dumps(jsonable_encoder(value)))


async def clear_cache(prefix, body):
    key = generate_key(prefix, body)
    keys = await redis.keys(f'{key}*')
    if keys:
        await redis.delete(*keys)
