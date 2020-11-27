from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from PIL import Image
from settings_bot_currency import TG_Token
from io import BytesIO
import os


def send_graph(bot, update):
    graph = open("graph.png", "rb")
    update.bot.send_photo(chat_id=bot.message.chat_id, photo=graph)
    print(bot.message.chat_id)

def main():
    print("photo")
    updater = Updater(token=TG_Token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("photo", send_graph))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
