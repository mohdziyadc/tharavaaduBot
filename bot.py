from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class TelegramBot:
    def __init__(self, botToken: str) -> None:
        self.bot = ApplicationBuilder().token(botToken).build()

    async def __hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'Yo wassup {update.effective_user.last_name}')

    def run(self):
        self.bot.add_handler(CommandHandler("hello", self.__hello))
        self.bot.run_polling()



