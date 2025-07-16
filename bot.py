from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from telebot.apihelper import ApiTelegramException

TOKEN = '8143002160:AAG2sHftRPtRNrj6pXYAiCWmlz2yW0hR6Hg'
bot = TeleBot(token=TOKEN)

questions = [
    {
        'question': 'Ո՞վ է համարվում գունավոր հեռուստատեսության ստեղծողներից մեկը։',
        'options': ['Ալեքսանդր Սահակյան', 'Երվանդ Լալայան', 'Հովհաննես Ադամյան', 'Անդրանիկ Օզանյան'],
        'correct_answer': 'Հովհաննես Ադամյան'
    },
    {
        'question': 'Ո՞ր բնագավառում է մասնագիտացած Ալեքսանդր Սահակյանը։',
        'options': ['Մաթեմատիկա', 'Բժշկություն', 'Քիմիա', 'Պատմություն'],
        'correct_answer': 'Քիմիա'
    },
    {
        'question': 'Ինչի՞ ուսումնասիրությամբ է զբաղվել Ալեքսանդր Սահակյանը։',
        'options': ['Թերմոդինամիկայով', 'Կենսաբանական նյութերով', 'Մետաղների հատկություններով', 'Լազերային տեխնոլոգիաներով'],
        'correct_answer': 'Մետաղների հատկություններով'
    },
    {
        'question': 'Ի՞նչ ոլորտում է գործել Ալեքսանդր Մանթաշյանցը։',
        'options': ['Գրականություն', 'Քաղաքագիտություն', 'Նավթարդյունաբերություն', 'Կենսաքիմիա'],
        'correct_answer': 'Նավթարդյունաբերություն'
    },
    {
        'question': 'Ո՞վ է աջակցել հայ ուսանողներին եվրոպական համալսարաններում ուսանելու հարցում։',
        'options': ['Հովհաննես Ադամյան', 'Ալեքսանդր Սահակյան', 'Անդրանիկ Օզանյան', 'Միքայել Նալբանդյան'],
        'correct_answer': 'Անդրանիկ Օզանյան'
    },
    {
        'question': 'Ո՞ր պատմաբանը ուսումնասիրել է հին աշխարհի պատմությունը։',
        'options': ['Երվանդ Լալայան', 'Միքայել Աթաբեկյան', 'Հակոբ Մանանդյան', 'Մանուկ Աբեղյան'],
        'correct_answer': 'Հակոբ Մանանդյան'
    },
    {
        'question': 'Ո՞վ է շեշտել գիտության դերը հասարակության մեջ։',
        'options': ['Անդրանիկ Օզանյան', 'Ալեքսանդր Մանթաշյանց', 'Միքայել Նալբանդյան', 'Հակոբ Մանանդյան'],
        'correct_answer': 'Միքայել Նալբանդյան'
    },
    {
        'question': 'Ո՞վ է հիմնել Էջմիածնի Հանրային թանգարանը։',
        'options': ['Հովհաննես Թումանյան', 'Մանուկ Աբեղյան', 'Երվանդ Լալայան', 'Միքայել Նալբանդյան'],
        'correct_answer': 'Երվանդ Լալայան'
    },
    {
        'question': 'Ո՞վ է արևմտահայ բժշկագիտության հիմնադիրներից։',
        'options': ['Ալեքսանդր Սահակյան', 'Մանուկ Աբեղյան', 'Միքայել Աթաբեկյան', 'Հովհաննես Ադամյան'],
        'correct_answer': 'Միքայել Աթաբեկյան'
    },
    {
        'question': 'Ո՞վ է ստեղծել հայագիտության գիտական հիմքերը։',
        'options': ['Երվանդ Լալայան', 'Հակոբ Մանանդյան', 'Մանուկ Աբեղյան', 'Անդրանիկ Օզանյան'],
        'correct_answer': 'Մանուկ Աբեղյան'
    }
]

def gen_markup(question):
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    for option in question['options']:
        markup.add(InlineKeyboardButton(option, callback_data=option))
    return markup



def check_answer(call, question):
    try:
        if call.data == question['correct_answer']:
            bot.answer_callback_query(call.id, "Շնորհավորում եմ, ճիշտ պատասխան!")
            bot.send_message(call.message.chat.id, "Դուք ճիշտ պատասխանեցիք!")
            return True
        else:
            bot.answer_callback_query(call.id, "Դուք սխալ պատասխան տվիք.")
            bot.send_message(call.message.chat.id, "Ցավոք, դուք սխալ պատասխանեցիք.")
            return False
    except ApiTelegramException as e:
        if 'query is too old' in str(e):
            print("Query expired, skipping response.")
        else:
            print(f"Error with callback query: {e}")


user_questions = {}
user_scores = {}

@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.chat.id
    user_questions[user_id] = 0
    user_scores[user_id] = 0  
    
    question = questions[user_questions[user_id]]
    bot.send_message(
        user_id,
        question['question'],
        reply_markup=gen_markup(question)
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    
    if user_id not in user_questions:
        bot.send_message(user_id, "Դուք պետք է սկսեք Quiz-ը նախապես '/start' հրամանը օգտագործելով.")
        return
    
    current_question = questions[user_questions[user_id]]
    
    if check_answer(call, current_question):
        user_scores[user_id] += 1 
    
    user_questions[user_id] += 1
    

    if user_questions[user_id] < len(questions):
        next_question = questions[user_questions[user_id]]
        bot.send_message(call.message.chat.id, next_question['question'], reply_markup=gen_markup(next_question))
    else:
        final_score = user_scores[user_id]
        bot.send_message(call.message.chat.id, f"Quiz-ը ավարտված է: Շնորհակալություն մասնակցության համար! Ձեր վերջնական արդյունքը: {final_score}/{len(questions)}")
        del user_questions[user_id]
        del user_scores[user_id]


bot.polling()