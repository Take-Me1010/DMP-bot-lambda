"""
このモジュールからコマンドを import することで、コマンドを登録できます。
>>> from commands import DiscordCommands
"""

import random

from discord_types import (
    DiscordCommandRequestBody,
    DiscordCommandResponseBody,
    DiscordResponseInteractionType,
)
from helpers import registerCommand


@registerCommand("coin", "コインを投げます。実行すると、表か裏が出ます。")
def throw_coin(body: DiscordCommandRequestBody) -> DiscordCommandResponseBody:
    result = {0: "表", 1: "裏"}[random.randrange(2)]

    return {
        "type": DiscordResponseInteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {"content": f"Result: {result}"},
    }


# def randint(options: list[dict[str, int]]):
#     result = random.randrange(
#         int(options[0]["value"]),
#         int(options[1]["value"]),
#     )

#     return result


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
