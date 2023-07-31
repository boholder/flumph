import os

import httpx
import openai
from loguru import logger

from duodrone import DuodroneConfig, OuterEvent

openai.api_key = os.environ['OPENAI_KEY']

duodrone_config = DuodroneConfig()


async def send(text: str):
    logger.info(f'active post:{text}')
    # resp = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hi!"}])
    async with httpx.AsyncClient() as client:
        # r = await client.post(url='http://localhost:1512', json=text)
        r = await client.post(url='https://httpbin.org/post', json=text)
        logger.info(f'active receive:{r}')
        duodrone_config.outer_event_handler(OuterEvent(r.text))
