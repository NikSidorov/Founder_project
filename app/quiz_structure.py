from database.database_structure import get_quiz_index, update_quiz_index
from app.keyboards import generate_options_keyboard
from log.quiz_answer import *
from log.quiz_question import *


async def get_question(message, user_id):

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_answers[current_question_index]['correct_option']
    opts = quiz_answers[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_questions[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index, right=0)
    await get_question(message, user_id)