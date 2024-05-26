from enum import Enum
import typing as tp


class DiscordCommands:
    registered_commands: tp.List["Command"] = []
    __unique_command_names: tp.Set[str] = set()

    @staticmethod
    def register(command: "Command"):
        if command.name in DiscordCommands.__unique_command_names:
            raise ValueError(f"Command name '{command.name}' is already registered.")
        DiscordCommands.registered_commands.append(command)
        DiscordCommands.__unique_command_names.add(command.name)

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

    def __init__(
        self,
        name: str,
        description: str,
        options: tp.List["DiscordApplicationCommandOption"],
    ) -> None:
        self.name = name
        self.description = description
        self.options = options

    @classmethod
    def New(
        cls,
        handler: CommandHandler,
        name: str,
        description: str,
        options: tp.List["DiscordApplicationCommandOption"] = [],
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


class DiscordApplicationCommandOptionType(int, Enum):
    """
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4  # Any integer between -2^53 and 2^53
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7  # Includes all channel types + categories
    ROLE = 8
    MENTIONABLE = 9  # Includes users and roles
    NUMBER = 10  # Any double between -2^53 and 2^53
    ATTACHMENT = 11  # attachment object


class DiscordApplicationCommandOptionChoice(tp.TypedDict):
    name: str
    value: tp.Union[str, int, float]


class _DiscordChannelType(int, Enum):
    """
    ref: https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    """

    GUILD_TEXT = 0  # a text channel within a server
    DM = 1  # a direct message between users
    GUILD_VOICE = 2  # a voice channel within a server
    GROUP_DM = 3  # a direct message between multiple users
    GUILD_CATEGORY = 4  # an organizational category that contains up to 50 channels
    GUILD_ANNOUNCEMENT = 5  # a channel that users can follow and crosspost into their own server (formerly news channels)
    ANNOUNCEMENT_THREAD = (
        10  # a temporary sub-channel within a GUILD_ANNOUNCEMENT channel
    )
    PUBLIC_THREAD = (
        11  # a temporary sub-channel within a GUILD_TEXT or GUILD_FORUM channel
    )
    PRIVATE_THREAD = 12  # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
    GUILD_STAGE_VOICE = 13  # a voice channel for hosting events with an audience
    GUILD_DIRECTORY = 14  # the channel in a hub containing the listed servers
    GUILD_FORUM = 15  # Channel that can only contain threads
    GUILD_MEDIA = (
        16  # Channel that can only contain threads, similar to GUILD_FORUM channels
    )


class _DiscordApplicationCommandOptionOptionals(tp.TypedDict, total=False):
    required: bool
    choices: tp.List[DiscordApplicationCommandOptionChoice]
    min_value: int
    max_value: int
    max_length: int  # valid only for `type = STRING (3)`

    channel_types: tp.List[_DiscordChannelType]

    name_localizations: tp.Dict[str, str]
    description_localizations: tp.Dict[str, str]

    autocomplete: bool


class DiscordApplicationCommandOption(_DiscordApplicationCommandOptionOptionals):
    """
    ref: https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    NOTE: Required options must be listed before optional options.
    """

    type: DiscordApplicationCommandOptionType
    name: str
    description: str


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


class DiscordCommandRequestBodyDataOption(tp.TypedDict):
    type: DiscordApplicationCommandOptionType
    name: str
    value: tp.Any  # NOTE: type depends on `type`. e.g. str, int, float


class DiscordCommandRequestBodyData(tp.TypedDict):
    id: tp.Any
    name: str
    options: tp.List[DiscordCommandRequestBodyDataOption]


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
