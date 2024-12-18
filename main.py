import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from aiogram.client.bot import DefaultBotProperties
import asyncio

# Токен вашего бота
API_TOKEN = '7712066245:AAHHkKuTRWW9VFk3wl6gxkBOWi679wfBg5c'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота и диспетчера
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Словарь для хранения состояний пользователей (для упрощения)
user_states = {}

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    # Текст сообщения
    text = ("<b>Приветствую!</b> 🖐\n\n"
            "Ты попал в самый мощный бесплатный продукт в телеграмме.\n\n"
            "Лично я благодаря этим знаниям, залил <b>больше</b> 20 миллионов рублей рекламного бюджета.\n\n"
            "➡️<b>Сейчас расскажу</b>, как тебе заработать в телеграмме 150к+ с нуля за месяц и узнать, как тебе масштабироваться ещё больше.\n\n"
            "<b>Поэтому, давай договоримся:</b>\n\n"
            "Ты тщательно изучаешь информацию и относишься к ней максимально серьёзно.\n\n"
            "<b>А в конце</b>, получаешь ценный подарок, который закроет все твои запросы.")

    # Ссылка на картинку
    photo_url = 'https://postimg.cc/hz6Gy2KN'  # Замените на правильную ссылку

    # Инлайн-кнопка
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="ПОГНАЛИ", callback_data="start_action")]]
    )

    # Отправляем фото и текст
    await bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=text, reply_markup=keyboard)


# Обработчик нажатия на инлайн-кнопку ПОГНАЛИ
@dp.callback_query(lambda callback_query: callback_query.data == "start_action")
async def handle_start_action(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)  # Ответ на callback
    text = ("<b>Недавно я окончил закуп каналу в тематике лайфхаков.</b> \n\n"
            "Привёл подписчика по 10р и клиент остался довольным. Теперь с этим человеком я работаю на постоянной основе. \n\n"
            "<b>Через 1 секунду приходит вопрос:</b>\n\n"
            "Как думаешь, какой бюджет закупа?")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="100-200к", callback_data="wrong_answer")],
            [InlineKeyboardButton(text="200-500к", callback_data="wrong_answer")],
            [InlineKeyboardButton(text="500-1млн", callback_data="wrong_answer")],
            [InlineKeyboardButton(text="2млн", callback_data="correct_answer")]
        ]
    )

    await bot.send_message(chat_id=callback_query.message.chat.id, text=text, reply_markup=keyboard)


# Обработчик неправильных ответов
@dp.callback_query(lambda callback_query: callback_query.data == "wrong_answer")
async def handle_wrong_answer(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Попробовать еще раз", callback_data="start_action")]]
    )
    await bot.send_message(chat_id=callback_query.message.chat.id, text="❌Неправильно", reply_markup=keyboard)


# Обработчик правильного ответа
@dp.callback_query(lambda callback_query: callback_query.data == "correct_answer")
async def handle_correct_answer(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Добавляем новый код перед отправкой первого урока
    # Сначала отправим сообщение "✅правильный ответ..." с кнопкой "готов"
    text_new = ("✅<b> Правильный ответ: 2.000.000р</b>\n\n"
                "Я уже не первый год в закупах и прекрасно понимаю, как тут зарабатывать больше 150к+\n\n"
                "Доказал я это не только на своем примере, но и на примере моих учеников, которых растил с нуля.\n\n"
                "<b>Ну что, ты готов окунуться в мир телеграма и получить первый урок?</b>")
    keyboard_new = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="готов", callback_data="ready_for_info")]]
    )
    await bot.send_message(chat_id=callback_query.message.chat.id, text=text_new, reply_markup=keyboard_new, disable_web_page_preview=True)

    # Сохраняем в состояние, что пользователь прошел квиз, но еще не готов к уроку.
    user_states[callback_query.from_user.id] = {"quiz_passed": True, "ready_for_lesson": False}

    # Ниже - старый код, который не изменяем, но теперь перед его выполнением будет проверка состояния
    # Старый код урока (не меняем, не удаляем):
    text = ("💸<b>ПЕРВЫЙ УРОК [1/5]:</b> Кто такой закупщик рекламы? (Введение)\n\n"
            "Узнаешь, кто такой закупщик, как он зарабатывает и какие нужны навыки.\n\n"
            "<a href='https://vc.ru/1714540'><b>ПРОЧИТАТЬ</b></a> (2 минуты)")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Прочитал", callback_data="lesson_2")]]
    )

    # Добавляем проверку состояния, чтобы урок отправился только после нажатия "ДА!"
    # Если пользователь еще не готов к уроку, просто выйдем из функции не отправляя урок.
    if user_states.get(callback_query.from_user.id, {}).get("ready_for_lesson") is True:
        await bot.send_message(chat_id=callback_query.message.chat.id, text=text, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        # Если пользователь еще не готов, мы просто не отправляем урок здесь.
        # Старый код не удален, лишь дополнен условием.
        pass


# Хендлер для кнопки "готов" после правильного ответа
@dp.callback_query(lambda c: c.data == "ready_for_info")
async def handle_ready_for_info(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Сообщение с инструкциями
    text = ("<b>Прежде, чем я вышлю тебе первый урок — мне нужно узнать больше информации о тебе.</b>\n\n"
            "Чтобы помочь человеку стартануть в закупах, я должен понимать с чем он пришел.\n\n"
            "Отвечаю лично, полностью индивидуальный подход. Все конфиденциально.\n\n"
            "<b>Поэтому: очень важно, чтобы ты ответил на вопросы ниже</b>⬇️\n\n"
            "1. Как тебя зовут? Сколько лет? В каком городе живешь?\n\n"
            "2. Чем занимаешься? Работаешь/учишься, расскажи подробнее\n\n"
            "3. Сколько зарабатываешь сейчас? Сколько хотела бы зарабатывать?\n\n"
            "4. Был ли опыт в том, чтобы построить свой бизнес? Не обязательно на запусках.\n\n"
            "<b>Ответы присылай мне в личку:</b> @Arti_Guru")
    await bot.send_message(chat_id=callback_query.message.chat.id, text=text, disable_web_page_preview=True)

    # Ждем 5 секунд
    await asyncio.sleep(300)

    # После 5 секунд отправляем сообщение с картинкой и кнопкой "ДА!"
    photo_url = 'https://postimg.cc/cgg9YBTF'  # Замените ссылку на нужную
    text2 = "Ответы отправлены? Можем стартовать?"
    keyboard_yes = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="ДА!", callback_data="start_lessons")]]
    )
    await bot.send_photo(chat_id=callback_query.message.chat.id, photo=photo_url, caption=text2, reply_markup=keyboard_yes)


# Хендлер для кнопки "ДА!" для старта урока
@dp.callback_query(lambda c: c.data == "start_lessons")
async def handle_start_lessons(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Обновляем состояние, что пользователь теперь готов к уроку
    if callback_query.from_user.id in user_states:
        user_states[callback_query.from_user.id]["ready_for_lesson"] = True

    # Теперь мы вручную вызываем логику из правильного ответа еще раз, чтобы отправить первый урок.
    # По сути, повторяем код handle_correct_answer, но теперь пользователь "готов".
    # В handle_correct_answer код уже есть (мы его не меняем), поэтому просто вызываем ту же логику заново.
    # Но чтобы не дублировать, можно вызвать еще раз сам хендлер или скопировать тот же код.
    # Мы просто скопируем код отправки урока здесь, так как менять старый хендлер нельзя.

    text = ("💸<b>ПЕРВЫЙ УРОК [1/5]</b>: Кто такой закупщик рекламы? (Введение)\n\n"
            "Узнаешь, кто такой закупщик, как он зарабатывает и какие нужны навыки.\n\n"
            "<a href='https://vc.ru/1714540'><b>ПРОЧИТАТЬ</b></a> (2 минуты)")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Прочитал", callback_data="lesson_2")]]
    )

    await bot.send_message(chat_id=callback_query.message.chat.id, text=text, reply_markup=keyboard, disable_web_page_preview=True)


# Обработчик кнопки "Прочитал" для уроков
@dp.callback_query(lambda callback_query: callback_query.data.startswith("lesson_"))
async def handle_lessons(callback_query: CallbackQuery):
    lesson_data = {
        "lesson_2": {
            "text": ("💸<b>ВТОРОЙ УРОК [2/5]:</b> Как постянно находить клиентов? 2 способа.\n\n"
                     "Узнаешь, как находить платежеспособных клиентов, закрывать их и работать в долгосрок, постояно увеличивая бюджет.\n\n"
                     "<a href='https://vc.ru/1714604'><b>ПРОЧИТАТЬ</b></a> (3 минуты)"),
            "callback": "lesson_3"
        },
        "lesson_3": {
            "text": ("💸<b>ТРЕТИЙ УРОК [3/5]:</b> Как закупать ниже рынка и делать свою услугу качественно?\n\n"
                     "Узнаешь, как вести хороший пдп и оставлять приятное впечатление о себе.\n\n"
                     "<a href='https://vc.ru/1714851'><b>ПРОЧИТАТЬ</b></a> (2 минуты)"),
            "callback": "lesson_4"
        },
        "lesson_4": {
            "text": ("💸<b>ЧЕТВЁРТЫЙ УРОК [4/5]:</b> 2 этапа к масштабированию до 300 тысяч дохода.\n\n"
                     "Узнаешь, как с дохода 70-100к выйти на 300к+ и постоянно прогрессировать.\n\n"
                     "<a href='https://vc.ru/1714905'><b>ПРОЧИТАТЬ</b></a> (2 минуты)"),
            "callback": "lesson_5"
        },
        "lesson_5": {
            "text": ("💸<b>ПЯТЫЙ УРОК [5/5]:</b> Бесплатный разбор.\n\n"
                     "Прийти на разбор ко мне - самый быстрый способ начать делать деньги в телеграме.\n\n"
                     "➡️<b>Если ты новичок с небольшим доходом, то конкретно под твою ситуацию, мы распишем план выхода на первые 150к+</b>\n\n"
                     "➡️<b>Если ты уже делаешь 100-200к, то мы распишем план, как тебе делать в 3 раза больше.</b>\n\n"
                     "<b>Разбор</b> – это около 40 минут моего внимания и вовлечения в тебя.\n\n"
                     "<b>ЧТО БУДЕТ НА РАЗБОРЕ?</b>\n\n"
                     "— как тебе находить клиентов с бюджетом 300к+ каждую неделю.\n\n"
                     "— делюсь актуальными связками для заработка на закупах.\n\n"
                     "— как тебе строить стабильный и пассивный доход в тг.\n\n"
                     "— как качать медийку и увеличить репутацию.\n\n"
                     "— как оптимизировать работу, чтобы при минимальных усилиях, получать максимальный результат.\n\n"
                     "— строим конкретный план выхода на доход, именно для тебя.\n\n"
                     "<b>Пиши слово</b> \"разбор\" мне в личные сообщения и получай бесплатную консультацию: @Arti_Guru"),
            "callback": None
        }
    }

    lesson = lesson_data.get(callback_query.data)
    if lesson:
        keyboard = None
        if lesson["callback"]:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Прочитал", callback_data=lesson["callback"])]])

        await bot.send_message(chat_id=callback_query.message.chat.id, text=lesson["text"], reply_markup=keyboard, disable_web_page_preview=True)

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
