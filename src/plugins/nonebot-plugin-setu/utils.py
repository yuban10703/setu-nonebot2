import time
from io import BytesIO
from typing import Union

from PIL import Image
from nonebot.log import logger
from tenacity import retry, stop_after_attempt, wait_random

from .config import setu_config


def transpose_setu(setu: bytes) -> bytes:
    logger.info("翻转图片")
    raw = Image.open(BytesIO(setu))
    with BytesIO() as bf:
        raw.transpose(3).save(bf, format="png")
        return bf.getvalue()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random(min=1, max=2),
    retry_error_callback=lambda retry_state: "https://cdn.jsdelivr.net/gh/yuban10703/BlogImgdata/img/error.jpg",
)
async def download_setu(client, url) -> Union[bytes, str]:
    res = await client.get(url)
    if res.status_code != 200:
        logger.warning("download_setu: res.status_code != 200")
        raise Exception("download_setu: res.status_code != 200")
    with BytesIO() as bf:
        bf.write(res.content)
        if setu_config.transpose:
            return transpose_setu(bf.getvalue())
        bf.write(str(time.time()).encode("utf-8"))  # 增加信息,改变MD5
        return bf.getvalue()
