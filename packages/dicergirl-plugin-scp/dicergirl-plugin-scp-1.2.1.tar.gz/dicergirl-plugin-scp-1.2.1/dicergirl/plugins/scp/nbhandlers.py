from .agent import Agent
from .scpcards import scp_cards, scp_cache_cards
from .scputils import deal, begin
from .attributes import all_alias_dict

from dicergirl.utils.utils import format_msg, get_status, get_mentions, is_super_user
from dicergirl.handlers.on import on_startswith
from dicergirl.utils.parser import CommandParser, Commands, Only, Optional, Required, Positional
from nonebot.matcher import Matcher
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.internal.matcher.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent

import asyncio
import random

scpcommand = on_startswith(".scp", priority=1, block=True).handle()

async def scp_handler(matcher: Matcher, event: GroupMessageEvent):
    """ SCP 车卡指令 """
    if not get_status(event) and not event.to_me:
        return

    args = format_msg(event.get_message(), begin=".scp", zh_en=True)
    at = get_mentions(event)

    if at and not is_super_user(event):
        return "权限不足, 无法指定玩家修改人物卡."

    if at:
        qid = at[0]
    else:
        qid = ""

    cp = CommandParser(
        Commands([
            Only(("begin", "start", "起始")),
            Only(("level", "levelup", "lu", "权限")),
            Only(("reset", "r", "重置")),
            Only(("upgrade", "u", "up", "study", "升级", "学习")),
            Only(("deal", "d", "buy", "b", "购买")),
            Positional("first", cls=str),
            Positional("second", cls=str)
        ]),
        args=args,
        auto=True
    ).results

    if cp["begin"]:
        for des in begin():
            await matcher.send(des)
            await asyncio.sleep(2)
        return

    if cp["level"]:
        got = scp_cards.get(event, qid=qid)
        if not got:
            await matcher.send("你尚未保存人物卡, 请先保存人物卡.")
            return

        agt = Agent().load(got)

        if agt.ach >= 10:
            agt.ach -= 10
            agt.level += 1
            scp_cards.update(event, inv_dict=agt.__dict__, save=True)
            await matcher.send(f"{agt.name} 特工权限提升至 {agt.level} 级.")
            return
        else:
            await matcher.send(f"特工 {agt.name} 功勋不足, 无法申请提升权限等级.")
            return

    if cp["reset"]:
        agt = Agent().load(scp_cards.get(event, qid=qid))
        attr = cp["first"]

        if len(args) == 2:
            try:
                exec(f"agt.reset_{attr}()")
                scp_cards.update(event, agt.__dict__, qid=qid, save=True)
                await matcher.send(f"已重置指定人物卡属性: {attr}.")
            except:
                await matcher.send("指令看起来不存在.")
            finally:
                return

        agt.reset()
        scp_cards.update(event, agt.__dict__, qid=qid, save=True)
        await matcher.send(f"人物卡 {agt.name} 属性已重置.")
        return

    if cp["upgrade"]:
        agt = Agent().load(scp_cards.get(event, qid=qid))
        anb = agt.all_not_base()

        if cp["first"] in all_alias_dict.keys():
            key_name = all_alias_dict[cp["first"]]
            oldattr = getattr(agt, anb[key_name])
            level = int(oldattr[key_name])

            if len(args) <= 2:
                up = level + 1
            else:
                try:
                    up = int(cp["second"])
                except ValueError:
                    await matcher.send("需要提升的等级应当为整型数, 请检查你的指令.\n使用`.help scp`查看 SCP 车卡指令使用方法.")
                    return

            if level >= up:
                await matcher.send(f"你的 {cp['first']} 技能的等级已经是 {level} 级了.")
                return

            required = int(up * (up + 1) / 2 - level * (level + 1) / 2)
            if agt.p[anb[key_name]] < required:
                await matcher.send(f"你的熟练值不足以支撑你将 {cp['first']} 提升到 {up} 级.")
                return

            agt.p[anb[key_name]] -= required

            flt = random.randint(1, 10)

            if flt == 10:
                flt = 0

            oldattr[key_name] = float(up) + flt/10
            setattr(agt, anb[key_name], oldattr)
            scp_cards.update(event, agt.__dict__, qid=qid, save=True)
            await matcher.send(f"你的 {cp['first']} 升级到 {up} 级.\n该技能的熟练度为 {oldattr[key_name]}.")
        elif not cp["first"]:
            await matcher.send("请给出需要升级的技能, 使用`.help scp`获得帮助信息.")
        else:
            await matcher.send(f"自定义技能 {cp['first']} 无法被升级.")

        return

    if cp["deal"]:
        args_for_deal = args[1:]
        await matcher.send(deal(event, args_for_deal))
        return 

    agt = Agent()
    agt.init()

    scp_cache_cards.update(event, agt.__dict__, save=False)
    await matcher.send(str(agt.output()))

commands = {"scpcommand": "scp_handler"}