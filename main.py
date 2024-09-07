import os
from bot import TelegramBot
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN= os.getenv('BOT_TOKEN')


if __name__ == '__main__':
    bot = TelegramBot(BOT_TOKEN)
    bot.run()
