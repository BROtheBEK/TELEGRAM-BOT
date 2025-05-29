from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

BOT_TOKEN = '7836496490:AAF5tfPXGezyw0ARaUCNI6lm4xzVSOUChFo'
LINK = 'https://6e227b11-164f-4d7e-b97b-8177fd9b1ef1-00-12m9vq1a7q2w4.kirk.replit.dev/'

user_lang = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data='lang_uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')
        ]
    ]
    await update.message.reply_text(
        "Iltimos, tilni tanlang:\nПожалуйста, выберите язык:\nPlease select a language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data.split('_')[1]
    user_lang[query.from_user.id] = lang

    texts = {
        'uz': "Quyidagilardan birini tanlang:",
        'ru': "Выберите один из следующих:",
        'en': "Choose one of the following:"
    }

    buttons = {
        'uz': [
            [InlineKeyboardButton("📦 Buyurtma berish", web_app=WebAppInfo(url=LINK))],
            [InlineKeyboardButton("ℹ️ Biz haqimizda", callback_data='about')],
            [InlineKeyboardButton("📞 Creatorlar bilan bog‘lanish", callback_data='contact')]
        ],
        'ru': [
            [InlineKeyboardButton("📦 Сделать заказ", web_app=WebAppInfo(url=LINK))],
            [InlineKeyboardButton("ℹ️ О нас", callback_data='about')],
            [InlineKeyboardButton("📞 Связаться с креаторами", callback_data='contact')]
        ],
        'en': [
            [InlineKeyboardButton("📦 Make an order", web_app=WebAppInfo(url=LINK))],
            [InlineKeyboardButton("ℹ️ About us", callback_data='about')],
            [InlineKeyboardButton("📞 Contact the creators", callback_data='contact')]
        ]
    }

    await query.answer()
    await query.message.reply_text(
        texts[lang],
        reply_markup=InlineKeyboardMarkup(buttons[lang])
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = user_lang.get(query.from_user.id, 'uz')

    if query.data == 'about':
        texts = {
            'uz': "Biz haqimizda: Bu yerga siz haqingizda matn yozasiz.",
            'ru': "О нас: Здесь будет ваш текст о проекте.",
            'en': "About us: You can add your info here."
        }
        await query.answer()
        await query.message.reply_text(texts[lang])

    elif query.data == 'contact':
        texts = {
            'uz': "Creatorlar bilan bog‘lanish: Bu yerga kontaktlaringizni yozasiz.",
            'ru': "Связь с креаторами: Добавьте здесь свои контакты.",
            'en': "Contact the creators: Add your contact details here."
        }
        await query.answer()
        await query.message.reply_text(texts[lang])

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lang_selected, pattern=r'^lang_'))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern=r'^(about|contact)$'))

    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == '__main__':
    main()
