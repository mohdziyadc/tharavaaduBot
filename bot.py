from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
from actions import Actions


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, botToken: str) -> None:
        self.bot = ApplicationBuilder().token(botToken).build()

    async def __hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'Yo wassup {update.effective_user.last_name}')

    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        logger.info(f'User {user.first_name} started the conversation')

        keyboard = [[
            InlineKeyboardButton("Movie Recommendations", callback_data= "1")
            
        ], [InlineKeyboardButton("YT Recommendations", callback_data="2")
           ], [ InlineKeyboardButton("Grocery List", callback_data="3")
            ], [InlineKeyboardButton("Surprise Me", callback_data="4")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        img_url = "https://tharavaadu-tbot.s3.ap-south-1.amazonaws.com/IMG_0800.jpg"
        tagline = "Welcome to Tharavaadu 🏠\n\nWhat are u feeling today?👻 "
        await context.bot.send_photo(
            chat_id= update.message.chat_id,
            photo= img_url,
            caption= tagline,
            reply_markup=reply_markup
        )
       

    def run(self):
        self.bot.add_handler(CommandHandler("hello", self.__hello))
        self.bot.add_handler(CommandHandler("start", self.__start))
        self.bot.run_polling()



