from ast import pattern
from cgitb import text
from gc import callbacks
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, botToken: str) -> None:
        self.bot = ApplicationBuilder().token(botToken).build()
        self.movie_recoms, self.yt_recoms, self.grocery_list, self.surprise_me = range(
            4
        )
        self.START, self.GENRE_SELECT, self.END = range(3)

    async def __hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"Yo wassup {update.effective_user.last_name}")

    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        logger.info(f"User {user.first_name} started the conversation")

        keyboard = [
            [
                InlineKeyboardButton(
                    "Movie Recommendations", callback_data=str(self.movie_recoms)
                )
            ],
            [
                InlineKeyboardButton(
                    "YT Recommendations", callback_data=str(self.yt_recoms)
                )
            ],
            [
                InlineKeyboardButton(
                    "Grocery List", callback_data=str(self.grocery_list)
                )
            ],
            [InlineKeyboardButton("Surprise Me", callback_data=str(self.surprise_me))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        img_url = "https://tharavaadu-tbot.s3.ap-south-1.amazonaws.com/IMG_0800.jpg"
        tagline = "Welcome to Tharavaadu 🏠\n\nWhat are u feeling today?👻 "
        welcomeMsg = await update.message.reply_photo(
            caption=tagline, photo=img_url, reply_markup=reply_markup
        )
        context.user_data["message_id"] = welcomeMsg.message_id
        context.user_data["chat_id"] = welcomeMsg.chat_id
        return self.START

    async def showMovieGenres(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        movie_genres = ["Action", "Comedy", "Thriller"]
        keyboard = [
            [InlineKeyboardButton(genre, callback_data=str(genre))]
            for genre in movie_genres
        ]
        # keyboard.append([InlineKeyboardButton("Main Menu", callback_data="main_menu")])

        keyboard.append([InlineKeyboardButton("Exit", callback_data="exit")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        # await context.user_data.update(
        #     text="What would you like to see?", reply_markup=reply_markup
        # )
        # print(query)
        print("showMovieGenres called")
        # await query.edit_message_text("Helloo")
        await query.message.reply_text(
            text="What would you like to see?", reply_markup=reply_markup
        )
        # print(update.message.reply_text("Hello"))
        return self.GENRE_SELECT

    async def recommendMovies(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("recommendMovies called")
        query = update.callback_query
        await query.answer()

        data = query.data
        print(data)

        await query.message.reply_text(f"You have chosen {data} type of movies")
        return self.END

    # async def mainMenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     return self.START

    async def exit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("exit called")

        query = update.callback_query
        await query.answer()

        await query.message.reply_text("Byee Niggaa")
        return self.END

    def run(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.__start)],
            states={
                self.START: [
                    CallbackQueryHandler(
                        self.showMovieGenres,
                        pattern=("^" + str(self.movie_recoms) + "$"),
                    )
                ],
                self.GENRE_SELECT: [
                    CallbackQueryHandler(
                        self.recommendMovies,
                        pattern=("^" + "Action|Comedy|Thriller" + "$"),
                    ),
                    CallbackQueryHandler(
                        self.exit,
                        pattern=("^" + "exit" + "$"),
                    ),
                ],
                self.END: [
                    CallbackQueryHandler(
                        self.exit,
                        pattern=("^" + "exit" + "$"),
                    )
                ],
            },
            fallbacks=[CommandHandler("start", self.__start)],
        )

        self.bot.add_handler(CommandHandler("hello", self.__hello))
        self.bot.add_handler(conv_handler)
        # self.bot.add_handler(
        #     CallbackQueryHandler(self.showMovieGenres, pattern=str(self.movie_recoms))
        # )
        self.bot.run_polling()
