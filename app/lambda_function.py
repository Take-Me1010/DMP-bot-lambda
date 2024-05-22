import json

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

# コマンド登録とコマンド取得
from commands import DiscordCommands

from discord_types import (
    DiscordCommandRequestBody,
    DiscordCommandResponseBody,
    DiscordResponseInteractionType,
)
from lambda_types import (
    MyApiGatewayEvent,
    LambdaContext,
    MyApiGatewayResponse,
)
import helpers

PUBLIC_KEY = "3fd9b6ace7a15e9878d40e21f7e741ffb253a2dcae20f1db8d307bea272477b0"


def verify_request(event: MyApiGatewayEvent):
    """
    Verify the request signature.
    """
    signature = event["headers"]["x-signature-ed25519"]
    timestamp = event["headers"]["x-signature-timestamp"]

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    message = timestamp + event["body"]

    try:
        verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
    except BadSignatureError:
        return False

    return True


def discord_response(body: DiscordCommandRequestBody) -> MyApiGatewayResponse:
    name = body["data"]["name"]
    command = DiscordCommands.get(name)

    if command:
        res = command.handler(body)
    else:
        res: DiscordCommandResponseBody = {
            "type": DiscordResponseInteractionType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {"content": "Command not found."},
        }
    return helpers.toResponse(res)


def lambda_handler(
    event: MyApiGatewayEvent, context: LambdaContext
) -> MyApiGatewayResponse:
    """
    Entry point for AWS Lambda.
    """
    if not verify_request(event):
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("invalid request signature"),
        }

    body: DiscordCommandRequestBody = json.loads(event["body"])
    t = body["type"]
    if t == 1:
        # handle ping
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({"type": DiscordResponseInteractionType.PONG}),
        }
    elif t == 2:  # handle application command
        return discord_response(body)

    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("invalid request type"),
    }
