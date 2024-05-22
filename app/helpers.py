import json

from discord_types import (
    DiscordCommandResponseBody,
    Command,
    CommandHandler,
    DiscordCommands,
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


def registerCommand(name: str, description: str, options: list = []):
    def decorator(func: CommandHandler):
        c = Command.New(func, name, description, options)
        DiscordCommands.register(c)
        return c

    return decorator
