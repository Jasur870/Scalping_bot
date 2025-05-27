from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = '7706510531:AAEkT4uQ5O8nYLdHxGC-irIkSC9P6PHG0_4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.username or user.first_name or "Foydalanuvchi"
    message = f"Assalomu alaykum, @{name}!\nXush kelibsiz skalping signal botimizga!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()