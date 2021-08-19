# import nonebot
import re
from typing import Union

from nonebot import get_driver
from nonebot import on_regex
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageSegment, Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot import get_driver
import json
from pathlib import Path
from .config import Config
from .model import GetSetuConfig
from .setu import Setu
from .model import GroupConfig

driver = get_driver()

global_config = get_driver().config
config = Config(**global_config.dict())
digitalConversionDict = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}
callsetu = on_regex('来(.*?)[点丶、个份张幅](.*?)的?([rR]18)?[色瑟涩䔼😍🐍][图圖🤮]', priority=5)
# callsetu = on_regex('来(.*?)[点丶、个份张幅](.*?)的?([rR]18)?[s][t]', priority=5)


@callsetu.handle()
async def handle_first_receive(bot: Bot, event: Union[Event, GroupMessageEvent, PrivateMessageEvent], state: T_State):
    # print(state["_matched_groups"])
    # print(event.get_user_id())
    # print(event.message_type)
    # print(event.sub_type)
    # print(event.dict())
    # if isinstance(event, GroupMessageEvent):
    #     print(event.group_id)
    # elif isinstance(event, PrivateMessageEvent):
    #     print(event.sender.group_id)

    config_getSetu: GetSetuConfig = GetSetuConfig()
    info = state["_matched_groups"]
    if info[0] != "":
        if info[0] in digitalConversionDict.keys():
            config_getSetu.toGetNum = int(digitalConversionDict[info[1]])
        else:
            if info[0].isdigit():
                config_getSetu.toGetNum = int(info[0])
            else:
                await callsetu.send(MessageSegment.text('能不能用阿拉伯数字?'))
                logger.info('非数字')
                return None
    else:  # 未指定数量,默认1
        config_getSetu.toGetNum = 1
    config_getSetu.tags = [i for i in set(re.split(r"[,， ]", info[1])) if i != ""]
    if info[2]:  # r18关键字
        config_getSetu.level = 1
    await Setu(event, bot, config_getSetu).main()


@driver.on_bot_connect
async def buildConfig(bot: Bot):
    curFileDir = Path(__file__).absolute().parent  # 当前文件路径
    logger.info("开始更新所有群数据~")
    for group in await bot.get_group_list():
        groupid = group["group_id"]
        filePath = (
                curFileDir
                / "database"
                / "DB"
                / "configs"
                / "{}.json".format(groupid)
        )
        if filePath.is_file():
            logger.info("群:{} 配置文件已存在".format(groupid))
            continue
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(
                GroupConfig().dict(), f, indent=4, ensure_ascii=False
            )
        logger.success("%s.json创建成功" % groupid)
    logger.success("更新群信息成功~")
