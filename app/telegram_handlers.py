from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from .models import db, User, News
from sqlalchemy.exc import IntegrityError
from flask import current_app

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
MINI_APP_URL = os.getenv('WEBAPP_URL', '').strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.first_name or "کاربر گرامی"
    command = update.effective_message.text.split()

    if len(command) > 1 and command[1].startswith('news_'):
        news_id = command[1].replace('news_', '')
        with current_app.app_context():
            news = News.query.get(news_id)
            if news:
                read_url = f"{MINI_APP_URL}/read/{news_id}" if MINI_APP_URL else ""
                keyboard = [[InlineKeyboardButton("مشاهده خبر", web_app=WebAppInfo(url=read_url))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                caption = f"{news.title}\n\nبرای مشاهده کامل خبر، روی دکمه زیر کلیک کنید:"
                
                try:
                    await update.message.reply_photo(
                        photo=news.image_url,
                        caption=caption,
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    await update.message.reply_text(
                        f"خطا در بارگذاری تصویر.\n\n{caption}",
                        reply_markup=reply_markup
                    )
            else:
                await update.message.reply_text("متاسفانه خبر مورد نظر یافت نشد.")
    else:
        with current_app.app_context():
            try:
                db_user = User.query.filter_by(telegram_id=str(user.id)).first()
                if db_user is None:
                    db_user = User(telegram_id=str(user.id), username=user.username)
                    db.session.add(db_user)
                else:
                    db_user.username = user.username
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

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

def main(app) -> None:
    with app.app_context():
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.run_polling(allowed_updates=Update.ALL_TYPES)