import typing as tp
import json

from discord_types import (
    DiscordCommandResponseBody,
    Command,
    CommandHandler,
    DiscordCommands,
    DiscordApplicationCommandOption,
)
from lambda_types import MyApiGatewayResponse


def toResponse(
    body: DiscordCommandResponseBody, statusCode=200
) -> MyApiGatewayResponse:
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def registerCommand(
    name: str,
    description: str,
    options: list[DiscordApplicationCommandOption] = [],
):
    """convert a function to a command and register it by calling `DiscordCommands.register( func )`

    After decorating with this in command.py, you can access the function by `DiscordCommands.get(name)` as follows:
    >>> from commands import DiscordCommands
    >>> command = DiscordCommands.get(name)

    Args:
        name (str): name of the command
        description (str): description of the command
        options (tp.List[DiscordApplicationCommandOption], optional): options to determine its args. Defaults to [].

    Example:
    >>> @registerCommand("ping", "ping pong")
    >>> def ping(body: DiscordCommandRequestBody) -> DiscordCommandResponseBody:
    >>>     return {
    >>>         "type": InteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
    >>>         "data": {"content": "pong"},
    >>>     }
    """

    def decorator(func: CommandHandler):
        c = Command.New(func, name, description, options)
        DiscordCommands.register(c)
        return c

    return decorator
