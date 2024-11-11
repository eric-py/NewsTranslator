from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
MINI_APP_URL = os.getenv('WEBAPP_URL', '').strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.first_name or "کاربر گرامی"
    
    if MINI_APP_URL:
        keyboard = [[InlineKeyboardButton("مشاهده اخبار روز", web_app=WebAppInfo(url=MINI_APP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"سلام {username}!\n"
            "به ربات اخبار روز خوش آمدید. برای مشاهده آخرین اخبار و رویدادها، "
            "لطفاً روی دکمه زیر کلیک کنید:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            f"سلام {username}!\n"
            "متأسفانه در حال حاضر دسترسی به اخبار امکان‌پذیر نیست. "
            "لطفاً کمی بعد دوباره تلاش کنید."
        )

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)