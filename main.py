import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import  ReplyKeyboardBuilder
from aiogram import F
from log.quiz_answer import *
from log.quiz_question import *
from app.bot_settings import BOT_TOKEN
from database.database_structure import get_quiz_index, update_quiz_index, create_table
from app.quiz_structure import get_question, new_quiz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
# lets
right_answers = int

@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_answer[current_question_index]['correct_option']

    await callback.message.answer(f"Верно! Правильный ответ: {quiz_answer[current_question_index]['options'][correct_option]}")

    current_question_index = await get_quiz_index(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1

    # print(current_question_index)
    
    await update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(quiz_question):
        await get_question(callback.message, callback.from_user.id)
    else:
        # await get_result(callback.from_user.id)
        # res = (right_answers / current_question_index) * 100
        await callback.message.answer("Это был последний вопрос. Квиз завершен!"
                                      f"/n Ваш результат:  ")


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_answer[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_answer[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(quiz_question):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    
    await message.answer(f"Давайте начнем квиз!")

    await new_quiz(message)

async def main():

    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())