#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter


nonebot.init(_env_file=".env")

driver = nonebot.get_driver()

driver.register_adapter(Adapter)

# nonebot.load_builtin_plugins()
nonebot.load_plugins("src/plugins")

# app = nonebot.get_asgi()


if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run()
