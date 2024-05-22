"""
このモジュールからコマンドを import することで、コマンドを登録できます。
>>> from commands import DiscordCommands
"""

import random

from discord_types import (
    DiscordCommandRequestBody as RequestBody,
    DiscordCommandResponseBody as ResponseBody,
    DiscordResponseInteractionType as InteractionType,
    DiscordApplicationCommandOptionType as OptionType,
)
from helpers import registerCommand


@registerCommand("coin", "コインを投げます。実行すると、表か裏が出ます。")
def throw_coin(body: RequestBody) -> ResponseBody:
    result = {0: "表", 1: "裏"}[random.randrange(2)]

    return {
        "type": InteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {"content": f"Result: {result}"},
    }


@registerCommand(
    "randint",
    "0 ~ num - 1 でランダムな整数を返します。",
    options=[
        {
            "name": "num",
            "description": "乱数の最大値",
            "type": OptionType.INTEGER,
            "required": True,
        }
    ],
)
def randint(body: RequestBody) -> ResponseBody:
    num = body["data"]["options"][0]["value"]
    if not isinstance(num, int):
        return {
            "type": InteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {"content": "Invalid value."},
        }

    result = random.randrange(num)

    return {
        "type": InteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {"content": f"Result: {result}"},
    }


# def pick_up(options: list[str], n=1):
#     picked = []
#     while n > 0:
#         idx = random.randrange(len(options))
#         picked.append(options[idx])
#         options.pop(idx)
#         n -= 1

#     return picked


# def shuffle(options: list[str]):
#     _options = options.copy()
#     random.shuffle(_options)
#     return _options

# export DiscordCommands
from discord_types import DiscordCommands  # noqa
