from helpers import CommandData
from service_layer.commands_handlers.coinstatus import coinstatus_cmd
from service_layer.commands_handlers.give import give_cmd
from service_layer.commands_handlers.find import find_cmd

COMMANDS = [
    CommandData(
        callback=coinstatus_cmd,
        name="coinstatus",
        description="Shows the ammount of coins you currently have",
    ),
    CommandData(
        callback=give_cmd,
        name="give",
        description="Give coins to another user",
    ),
    CommandData(
        callback=find_cmd,
        name="find",
        description="Find id by username",
    ),
]
