import nonebot
from httpx_socks import AsyncProxyTransport
from nonebot.log import logger

global_config = nonebot.get_driver().config

if proxies_socks := global_config.proxies_socks:
    logger.info('已配置socks代理')
    transport = AsyncProxyTransport.from_url(proxies_socks)
    proxies = None
elif proxies_http := global_config.proxies_http:
    logger.info('已配置http代理')
    transport = None
    proxies = proxies_http
else:
    transport = None
    proxies = None
