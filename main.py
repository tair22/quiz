import telebot, os, random
from config import token
from collections import defaultdict
from logic import quiz_questions, MultipleChoiceQuestion

user_responses = {} 
points = defaultdict(int)
current_mc_questions = {}

bot = telebot.TeleBot(token)

def send_question(chat_id):
    current_question = quiz_questions[user_responses[chat_id]]
    
    if isinstance(current_question, MultipleChoiceQuestion):
        current_question.selected_answers = []
    
    image_path = f"D:/кодланд/bot roni/M2L3/{current_question.image_path}"
    with open(image_path, 'rb') as f:
        bot.send_photo(chat_id, f, current_question.text, reply_markup=current_question.gen_markup())

def move_to_next_question(chat_id):
    if user_responses[chat_id]>=len(quiz_questions):
        total_points = points[chat_id]
        total_questions = len(quiz_questions)
        bot.send_message(chat_id, "The end")
        result_message = f"Твой результат: {total_points} из {total_questions} очков!"
        bot.send_message(chat_id, result_message)
    else:
        send_question(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    current_question_index = user_responses[chat_id]
    current_question = quiz_questions[current_question_index]

    if call.data.startswith("mc_"):
        if call.data == "mc_submit":
            try:
                bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
            except Exception as e:
                print(f"Ошибка при удалении клавиатуры: {e}")

            if current_question.check_answers():
                bot.answer_callback_query(call.id, "Все ответы правильные! 🎉")
                points[chat_id] += 1
            else:
                bot.answer_callback_query(call.id, "Не все ответы правильные")
            
            user_responses[chat_id] += 1
            move_to_next_question(chat_id)
            
        else:
            answer_index = int(call.data.split("_")[1])
            current_question.toggle_answer(answer_index)
            
            
            try:
                bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    reply_markup=current_question.gen_markup()
                )
                bot.answer_callback_query(call.id, "Ответ обновлен")
            except Exception as e:
                print(f"Ошибка при обновлении клавиатуры: {e}")
    
    elif call.data == "correct":
        try:
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=call.message.message_id,
                reply_markup=None
            )
        except Exception as e:
            print(f"Ошибка при удалении : {e}")

        bot.answer_callback_query(call.id, "Answer is correct")
        points[chat_id] += 1
        user_responses[chat_id] += 1
        move_to_next_question(chat_id)

    elif call.data == "wrong":
        try:
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=call.message.message_id,
                reply_markup=None
            )
        except Exception as e:
            print(f"Ошибка при удалении клавиатуры: {e}")

        bot.answer_callback_query(call.id, "Answer is wrong")
        user_responses[chat_id] += 1
        move_to_next_question(chat_id)

@bot.message_handler(commands=['start'])
def start(message):
        user_responses[message.chat.id] = 0
        points[message.chat.id] = 0
        send_question(message.chat.id)

bot.infinity_polling()