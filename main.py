import os
import logging
from bot import TelegramBot
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN= os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

if __name__ == '__main__':
    bot = TelegramBot(BOT_TOKEN)
    bot.run()
