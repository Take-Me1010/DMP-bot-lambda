from enum import Enum
import typing as tp


class DiscordCommands:
    registered_commands: tp.List["Command"] = []

    @staticmethod
    def register(command: "Command"):
        DiscordCommands.registered_commands.append(command)

    @staticmethod
    def get_commands():
        return DiscordCommands.registered_commands

    @staticmethod
    def get(name: str):
        for command in DiscordCommands.registered_commands:
            if command.name == name:
                return command
        return None


class CommandHandler(tp.Protocol):
    def __call__(
        self, body: "DiscordCommandRequestBody"
    ) -> "DiscordCommandResponseBody": ...


class Command:
    handler: CommandHandler

    def __init__(self, name: str, description: str, options: tp.List[str]) -> None:
        self.name = name
        self.description = description
        self.options = options

    @classmethod
    def New(
        cls,
        handler: CommandHandler,
        name: str,
        description: str,
        options: tp.List[str] = [],
    ):
        instance = cls(name, description, options)
        instance.handler = handler
        return instance

    def toDict(self):
        d: dict[str, tp.Any] = {
            "name": self.name,
            "description": self.description,
        }
        if self.options:
            d["options"] = self.options
        return d


class DiscordRequestInteractionType(int, Enum):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    NOTE: for Enum to become Serializable, it must be a subclass of int (ref: https://qiita.com/hoto17296/items/abb9ad35d4d93489f6aa)
    """

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class DiscordResponseInteractionType(int, Enum):
    """
    NOTE: for Enum to become Serializable, it must be a subclass of int (ref: https://qiita.com/hoto17296/items/abb9ad35d4d93489f6aa)
    """

    PONG = 1  # ACK a Ping
    CHANNEL_MESSAGE_WITH_SOURCE = 4  # respond to an interaction with a message
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = (
        5  # ACK an interaction and edit a response later, the user sees a loading state
    )
    DEFERRED_UPDATE_MESSAGE = 6  # for components, ACK an interaction and edit the original message later; the user does not see a loading state
    UPDATE_MESSAGE = 7  # for components, edit the message the component was attached to
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = (
        8  # respond to an autocomplete interaction with suggested choices
    )
    MODAL = 9  # respond to an interaction with a popup modal
    PREMIUM_REQUIRED = 10  # respond to an interaction with an upgrade button, only available for apps with monetization enabled


class DiscordCommandRequestBodyData(tp.TypedDict):
    id: tp.Any
    name: str
    options: tp.List[tp.Dict[str, tp.Any]]


class DiscordCommandRequestBody(tp.TypedDict):
    type: tp.Literal[
        DiscordRequestInteractionType.PING,
        DiscordRequestInteractionType.APPLICATION_COMMAND,
    ]

    # only for `APPLICATION_COMMAND`
    data: DiscordCommandRequestBodyData


class DiscordCommandResponseBody(tp.TypedDict):
    type: DiscordResponseInteractionType
    # ref: https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure
    data: tp.Dict[tp.Literal["content"], str]
