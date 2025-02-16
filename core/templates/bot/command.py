from telegram import BotCommand

NO_ACCESS_COMMANDS = [BotCommand("start", "start the bot")]
HAS_ACCESS_COMMANDS = [
    BotCommand("start", "start the bot"),
]
