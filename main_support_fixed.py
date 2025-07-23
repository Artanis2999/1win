import logging
import json
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import FSInputFile, WebAppInfo
from dotenv import load_dotenv
import os
import asyncio
from check_reg import check_user_registered
from check_dep import check_user_deposited


# Загрузка конфигурации
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Загрузка переводов
with open(Path(__file__).parent / 'translations.json', 'r', encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

REG_CHANNEL_ID = -1002777437965

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Конфигурация
CHANNEL_ID = -1001988478879
CHANNEL_LINK = "https://t.me/+QBQhn_Xqvio1Zjcy"
P_LINK = "https://1wcjlr.com/casino/list?open=register&p=kd4s&sub1="
IMAGE_PATH = Path(__file__).parent / "assets/main_menu.jpg"
BOT_DESCRIPTION = "Aviamasters - your aviation helper ✈️"
USERS_FILE = Path(__file__).parent / 'users.json'

# Настройки языков
LANGUAGES = {
    "ru": {"name": "Русский", "flag": "🇷🇺"},
    "en": {"name": "English", "flag": "🇬🇧"},
    "hi": {"name": "हिन्दी", "flag": "🇮🇳"},
    "id": {"name": "Bahasa", "flag": "🇮🇩"},
    "pt": {"name": "Português", "flag": "🇧🇷"},
    "vi": {"name": "Tiếng Việt", "flag": "🇻🇳"},
    "uk": {"name": "Українська", "flag": "🇺🇦"},
    "fr": {"name": "Français", "flag": "🇫🇷"}
}

# Хранилище данных пользователя
user_data = {}

from aiogram.types import WebAppInfo

async def show_main_menu(chat_id: int, lang: str = "en", message_id: int = None):
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    try:
        # Получаем роль из users.json
        is_admin = False
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for u in data.get("users", []):
                if u["id"] == chat_id:
                    is_admin = u.get("admin", False)
                    break

        web_url = "https://avia1win.netlify.app/frontend/admin" if is_admin else "https://avia1win.netlify.app/frontend"
        photo = FSInputFile(IMAGE_PATH)
        builder = ReplyKeyboardBuilder()

        builder.row(
            types.KeyboardButton(text=translations.get("reg", "📝 Registration")),
            types.KeyboardButton(text=translations.get("instr", "📚 Instructions"))
        )
        builder.row(types.KeyboardButton(text=translations.get("support", "🛠 Support")))
        builder.row(types.KeyboardButton(
            text="🚀 Получить сигнал",
            web_app=WebAppInfo(url=web_url)
        ))

        if message_id:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        sent_message = await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=f"<b>{translations.get('menu', 'Main Menu')}</b>",
            parse_mode="HTML",
            reply_markup=builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        return sent_message.message_id
    except Exception as e:
        logging.error(f"Error showing menu: {e}")

        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text=translations.get("reg", "📝 Registration")),
            types.KeyboardButton(text=translations.get("instr", "📚 Instructions"))
        )
        builder.row(types.KeyboardButton(text=translations.get("support", "🛠 Support")))
        builder.row(types.KeyboardButton(
            text="🚀 Получить сигнал",
            web_app=WebAppInfo(url="https://avia1win.netlify.app/frontend")
        ))

        if message_id:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        sent_message = await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{translations.get('menu', 'Main Menu')}</b>",
            parse_mode="HTML",
            reply_markup=builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        return sent_message.message_id
    except Exception as e:
        logging.error(f"Error showing menu: {e}")
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text=translations.get("reg", "📝 Registration")),
            types.KeyboardButton(text=translations.get("instr", "📚 Instructions"))
        )
        builder.row(types.KeyboardButton(text=translations.get("support", "🛠 Support")))
        builder.row(types.KeyboardButton(
            text="🚀 Получить сигнал",
            web_app=WebAppInfo(url="https://avia1win.netlify.app")  # ← сюда тоже
        ))

        if message_id:
            
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        sent_message = await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{translations.get('menu', 'Main Menu')}</b>",
            parse_mode="HTML",
            reply_markup=builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        return sent_message.message_id


async def show_registration(chat_id: int, lang: str = "en", message_id: int = None, user_id: int = None):
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    # Формируем персонализированную ссылку с ID пользователя
    personalized_link = f"{P_LINK}{user_id}"
    # Заменяем PERSONAL_LINK в сообщении на персонализированную ссылку
    registration_message = translations.get("registration_message", "Registration message").replace("PERSONAL_LINK", personalized_link)
    
    try:
        photo = FSInputFile(IMAGE_PATH)
        builder = ReplyKeyboardBuilder()
        
        builder.row(types.KeyboardButton(text=translations.get("next", "➡️ Next")))
        builder.row(types.KeyboardButton(text=translations.get("back", "⬅️ Back")))
        
        if message_id:
              # Задержка 2 секунды
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            
        sent_message = await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=registration_message,
            parse_mode="HTML",
            reply_markup=builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        return sent_message.message_id
    except Exception as e:
        logging.error(f"Error showing registration: {e}")
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text=translations.get("next", "➡️ Next")))
        builder.row(types.KeyboardButton(text=translations.get("back", "⬅️ Back")))
        
        if message_id:
              # Задержка 2 секунды
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            
        sent_message = await bot.send_message(
            chat_id=chat_id,
            text=registration_message,
            parse_mode="HTML",
            reply_markup=builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        return sent_message.message_id


@dp.message(lambda m: m.text in [TRANSLATIONS[lang]["next"] for lang in LANGUAGES])
async def process_next(message: types.Message):
    user = message.from_user
    user_id = user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    translations = TRANSLATIONS[lang]
    stage = user_data.get(user_id, {}).get("last_stage")

    try:
        if stage == "registration":
            if await check_user_registered(user_id):
                # Обновляем stage в users.json
                with open(USERS_FILE, 'r+', encoding='utf-8') as f:
                    data = json.load(f)
                    for u in data["users"]:
                        if u["id"] == user_id:
                            u["stage"] = "deposit"
                            break
                    f.seek(0)
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.truncate()

                user_data[user_id]["last_stage"] = "deposit"
                builder = ReplyKeyboardBuilder()
                builder.row(
                    types.KeyboardButton(text=translations["next"]),
                    types.KeyboardButton(text=translations["back"])
                )
                await message.answer(translations["dep"], reply_markup=builder.as_markup(resize_keyboard=True))
            else:
                await message.answer("❌ Вы не зарегистрированы! Сначала пройдите регистрацию.")
        elif stage == "deposit":
            if await check_user_deposited(user_id):
                await message.answer("✅ Депозит подтвержден. Продолжаем...")
                user_data[user_id]["last_message_id"] = await show_main_menu(user_id, lang)

            else:
                await message.answer("❌ Мы не нашли депозит. Убедитесь, что вы пополнили аккаунт и попробуйте позже.")
        else:
            await message.answer("⚠️ Неизвестный этап. Начните с /start.")
    except Exception as e:
        logging.error(f"Ошибка при обработке этапа {stage}: {e}")
        await message.answer("⚠️ Ошибка. Попробуйте позже.")
    user = message.from_user
    lang = user_data.get(user.id, {}).get("lang", "en")
    translations = TRANSLATIONS[lang]


def register_user_if_new(user: types.User):
    USERS_FILE = Path(__file__).parent / 'users.json'
    try:
        with open(USERS_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            user_ids = [u["id"] for u in data.get("users", [])]
            if user.id not in user_ids:
                new_user = {
                    "id": user.id,
                    "name": user.full_name,
                    "username": user.username or "",
                    "reg": False,
                    "dep": False,
                    "admin": False,
                    "amount": 0
                }
                data["users"].append(new_user)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
    except Exception as e:
        logging.error(f"Ошибка при регистрации пользователя: {e}")



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    register_user_if_new(message.from_user)
    builder = InlineKeyboardBuilder()
    
    for i in range(0, len(LANGUAGES), 2):
        languages = list(LANGUAGES.items())
        row = languages[i:i+2]
        
        for code, info in row:
            builder.button(
                text=f"{info['flag']} {info['name']}", 
                callback_data=f"lang_{code}"
            )
        
        builder.adjust(2)
    
    await message.answer(
        TRANSLATIONS["en"]["welcome"],
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data.startswith("lang_"))
async def process_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_data[callback.from_user.id] = {"lang": lang}
    
    await callback.message.delete()
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=translations["subscribe_btn"],
            url=CHANNEL_LINK
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=translations["check"],
            callback_data="check_subscription"
        )
    )
    
    await callback.message.answer(
        translations["subscribe"],
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            await callback.message.delete()
            
            temp_msg = await callback.message.answer(translations["access_granted"])
            
            await temp_msg.delete()
            
            user_data[user_id]["last_message_id"] = await show_main_menu(user_id, lang)
        else:
            await callback.answer(translations["not_subscribed"], show_alert=True)
    except Exception as e:
        logging.error(f"Subscription error: {e}")
        await callback.answer(translations["check_error"], show_alert=True)


@dp.message(lambda message: message.text in [TRANSLATIONS[lang]["reg"] for lang in LANGUAGES])
async def process_registration_button(message: types.Message):
    user_id = message.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    last_message_id = user_data.get(user_id, {}).get("last_message_id")
    if last_message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_message_id)
        except Exception as e:
            logging.error(f"Error deleting main menu message: {e}")
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    user_data[user_id]["last_message_id"] = await show_registration(user_id, lang, user_id=user_id)
    user_data[user_id]["last_stage"] = "registration"

@dp.message(lambda message: message.text in [TRANSLATIONS[lang]["algo"] for lang in LANGUAGES])
async def process_algo_button(message: types.Message):
    user_id = message.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    last_message_id = user_data.get(user_id, {}).get("last_message_id")
    if last_message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_message_id)
        except Exception as e:
            logging.error(f"Error deleting main menu message: {e}")
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    user_data[user_id]["last_message_id"] = await show_main_menu(user_id, lang)

@dp.message(lambda message: message.text in [TRANSLATIONS[lang]["support"] for lang in LANGUAGES])
async def process_support(message: types.Message):
    user_id = message.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=translations.get("reg", "📝 Registration")),
        types.KeyboardButton(text=translations.get("instr", "📚 Instructions"))
    )
    builder.row(types.KeyboardButton(text=translations.get("support", "🛠 Support")))
    builder.row(types.KeyboardButton(
        text="🚀 Получить сигнал",
        web_app=WebAppInfo(url="https://avia1win.netlify.app/frontend")
    ))

    await message.answer(
        translations.get("support_text", "Свяжитесь с поддержкой: @maboy_poderzhka"),
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message(lambda message: message.text in [TRANSLATIONS[lang]["back"] for lang in LANGUAGES])
async def process_back(message: types.Message):
    user_id = message.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en")
    
    # Удаляем сообщение с кнопкой "Назад"
      # Задержка 2 секунды
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    # Удаляем предыдущее сообщение (регистрации)
    last_message_id = user_data.get(user_id, {}).get("last_message_id")
    if last_message_id:
        try:
              # Задержка 2 секунды
            await bot.delete_message(chat_id=user_id, message_id=last_message_id)
        except Exception as e:
            logging.error(f"Error deleting registration message: {e}")
    
    # Показываем главное меню
    user_data[user_id]["last_message_id"] = await show_main_menu(user_id, lang)

async def set_bot_description():
    await bot.set_my_description(BOT_DESCRIPTION)

async def main():
    await set_bot_description()
    await dp.start_polling(bot)

@dp.message(lambda message: message.text in [TRANSLATIONS[lang]["instr"] for lang in LANGUAGES])
async def process_instruction(message: types.Message):
    user_id = message.from_user.id
    lang = user_data.get(user_id, {}).get("lang", "en") 
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=translations.get("reg", "📝 Registration")),
        types.KeyboardButton(text=translations.get("instr", "📚 Instructions"))
    )
    builder.row(types.KeyboardButton(text=translations.get("support", "🛠 Support")))
    builder.row(types.KeyboardButton(
        text="🚀 Получить сигнал",
        web_app=WebAppInfo(url="https://avia1win.netlify.app/frontend")
    ))

    await message.answer(
        translations.get("instructions", "Инструкция недоступна"),
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

if __name__ == "__main__":
    asyncio.run(main())  

