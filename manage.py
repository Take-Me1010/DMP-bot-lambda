"""
ref: https://discord.com/developers/docs/interactions/application-commands#slash-commands
"""

import os
import sys
import json

import requests

# HACK
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
import app.commands


APP_ID = os.environ["APP_ID"]
SERVER_ID = os.environ["SERVER_ID"]
BOT_TOKEN = os.environ["BOT_TOKEN"]


def confirm():
    print("ok? (y/n)")
    if input() != "y":
        return False
    return True


def register():
    payload = [
        command.toDict() for command in app.commands.DiscordCommands.get_commands()
    ]

    print("Try to register the following commands:\n")
    for p in payload:
        print(p)
    print(f"\nTotal: {len(payload)}")

    if not confirm():
        return

    # global commands
    # url = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

    # server commands
    url = (
        f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{SERVER_ID}/commands"
    )

    response = requests.put(
        url, headers={"Authorization": f"Bot {BOT_TOKEN}"}, json=payload
    )

    with open("registered_commands.json", "w") as f:
        json.dump(
            {
                "statusCode": response.status_code,
                "body": response.json(),
            },
            f,
            ensure_ascii=False,
            indent=4,
        )

    print(
        "Registered commands and saved the response to 'registered_commands.json' file."
    )


def remove(name: str):
    # global commands
    # url = f'https://discord.com/api/v10/applications/{APP_ID}/commands/{name}'

    # server commands
    url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{SERVER_ID}/commands/{name}"

    response = requests.delete(url, headers={"Authorization": f"Bot {BOT_TOKEN}"})

    print(response.json())


def main(*args: str):
    if "-Remove" in args and len(args) == 2:
        remove(args[1])

    else:
        register()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        main()
