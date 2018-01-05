import sys
from io import BytesIO

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Message

from flask import Flask, request, send_file

from fsm import TocMachine, init, print_something
from transitions import State

import random

API_TOKEN = '408775585:AAH-zUurs9tNkV_qbfSyFz3EPztGWGABEF8'
WEBHOOK_URL = 'https://67450858.ngrok.io/hook'
edited_msg = None

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        State(name="start", on_enter=['start_msg']),
        # joke
        State(name="joke", on_enter=['give_joke']),
        State(name="comment_joke"),
        State(name="question_joke"),
        # riddle
        State(name="riddle", on_enter=['give_riddle']),
        State(name="answer_riddle", on_enter=['answer_riddle']),
        State(name="question_riddle"),
        # music
        State(name="question_music", on_enter=['question_music']),
        # music -> suggest
        State(name="question_mood_suggest", on_enter=['question_mood']),
        State(name="mood_music", on_enter=['mood_music']),
        State(name="suggest_next"),
        # music -> search
        State(name="search", on_enter=['search']),
        State(name="result_and_question", on_enter=['result_and_question']),
        State(name="happy_result"),
        # chat
        State(name="question_mood_chat", on_enter=['chat_question_mood']),
        State(name="give_pic_or_text", on_enter=['pic_or_text']),
        State(name="question_better", on_enter=['question_better']),
        State(name="chat_deeply", on_enter=['chat_deeply'])
    ],
    transitions=[
        # joke
        {
            'trigger': 'start_to_joke',
            'source': 'start',
            'dest': 'joke',
        },
        {
            'trigger': 'joke_to_comment',
            'source': 'joke',
            'dest': 'comment_joke',
            'conditions': 'comment_joke'
        },
        {
            'trigger': 'comment_joke_to_question',
            'source': 'comment_joke',
            'dest': 'question_joke',
            # jump directly
        },
        {
            'trigger': 'next_joke',
            'source': 'question_joke',
            'dest': 'joke',
            'conditions': 'question_joke'
        },
        {
            'trigger': 'next_joke',
            'source': 'question_joke',
            'dest': 'start',
            'unless': 'question_joke'
        },
        # riddle
        {
            'trigger': 'start_to_riddle',
            'source': 'start',
            'dest': 'riddle',
        },
        {
            'trigger': 'riddle_to_answer',
            'source': 'riddle',
            'dest': 'answer_riddle',
        },
        {
            'trigger': 'answer_riddle_to_question',
            'source': 'answer_riddle',
            'dest': 'question_riddle',
        },
        {
            'trigger': 'next_riddle',
            'source': 'question_riddle',
            'dest': 'riddle',
            'conditions': 'question_riddle'
        },
        {
            'trigger': 'next_riddle',
            'source': 'question_riddle',
            'dest': 'start',
            'unless': 'question_riddle'
        },
        # music
        {
            'trigger': 'start_to_music',
            'source': 'start',
            'dest': 'question_music',
        },
        {#suggest
            'trigger': 'music_reply',
            'source': 'question_music',
            'dest': 'question_mood_suggest',
            'conditions': 'where_music'
        },
        {
            'trigger': 'suggest_mood_music',
            'source': 'question_mood_suggest',
            'dest': 'mood_music',
        },
        {
            'trigger': 'suggest_next_music',
            'source': 'mood_music',
            'dest': 'suggest_next',
        },
        {
            'trigger': 'next_suggest',
            'source': 'suggest_next',
            'dest': 'question_mood_suggest',
            'conditions': 'suggest_next'
        },
        {
            'trigger': 'next_suggest',
            'source': 'suggest_next',
            'dest': 'start',
            'unless': 'suggest_next'
        },
        {# search
            'trigger': 'music_reply',
            'source': 'question_music',
            'dest': 'search',
            'unless': 'where_music'
        },
        {
            'trigger': 'search_result_and_question',
            'source': 'search',
            'dest': 'result_and_question',
        },
        {
            'trigger': 'question_result',
            'source': 'result_and_question',
            'dest': 'happy_result',
        },
        {
            'trigger': 'search_next',
            'source': 'happy_result',
            'dest': 'search',
            'conditions': 'happy_result'
        },
        {
            'trigger': 'search_next',
            'source': 'happy_result',
            'dest': 'start',
            'unless': 'happy_result'
        },
        # chat
        {
            'trigger': 'start_to_chat',
            'source': 'start',
            'dest': 'question_mood_chat',
        },
        {
            'trigger': 'chat_with_mood',
            'source': 'question_mood_chat',
            'dest': 'give_pic_or_text',
        },
        {
            'trigger': 'mood_be_better',
            'source': 'give_pic_or_text',
            'dest': 'question_better',
            'conditions': 'be_better'
        },
        {
            'trigger': 'next_chat',
            'source': 'question_better',
            'dest': 'question_mood_chat',
            'conditions': 'pic_again'
        },
        {
            'trigger': 'next_chat',
            'source': 'question_better',
            'dest': 'start',
            'unless': 'pic_again'
        },
        {
            'trigger': 'mood_be_better',
            'source': 'give_pic_or_text',
            'dest': 'chat_deeply',
            'unless': 'be_better'
        }
    ],
    initial='start',
    auto_transitions=True,
    show_conditions=True,
    ignore_invalid_triggers=True,
)



def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))

@app.route('/hook', methods=['POST'])
def webhook_handler():
    
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # print message
    if update.callback_query != None:
        print("\033[1;34m""user: ", end='')
        print_something(update.callback_query.from_user)
        print("Text: " + update.callback_query.message.text + "\nData:" + update.callback_query.data + "\n")
        if update.callback_query.message.entities != []:
            print("Entities: ", end='')
            print_something(update.callback_query.message.parse_entities())
        if update.callback_query.message.photo != []:
            print("Photo: ", end='')
            print_something(update.callback_query.message.photo)
        print("\033[m""")
    else:
        print("\033[1;34m""user: ", end='')
        print_something(update.message.from_user)
        print("Text: " + update.message.text + "\nData:" + "\n")
        if update.message.entities != []:
            print("Entities: ", end='')
            print_something(update.message.parse_entities())
        if update.message.photo != []:
            print("Photo: ", end='')
            print_something(update.message.photo)
        if update.message.sticker != None:
            print("Sticker: ", end='')
            print_something(update.message.sticker)
        print("\033[m""")

    #print(update)

    # Just jugde state here.
    if update.callback_query != None:
        # callback enter here
        if machine.is_start():
            if update.callback_query != None: 
                if update.callback_query.data == "Joke":
                    machine.start_to_joke(update)
                elif update.callback_query.data == "Riddle":
                    machine.start_to_riddle(update)
                elif update.callback_query.data == "Video":
                    machine.start_to_music(update)
                elif update.callback_query.data == "Chat":
                    machine.start_to_chat(update)
                else:
                    # error botton input will cause msg be deleted.
                    update.callback_query.message.edit_reply_markup(reply_markup=None)
                    print("\033[0;32;31m""error: delete this markup""\033[m")
        elif machine.is_joke():
            data = update.callback_query.data
            if data in ["Bad", "Normal", "Funny"]:
                machine.joke_to_comment(update)
                machine.comment_joke_to_question(update) # jump directly
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: joke delete""\033[m")

        elif machine.is_question_joke():
            data = update.callback_query.data
            if data in ["Next joke", "Back"]:
                machine.next_joke(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: joke question delete""\033[m")

        elif machine.is_question_riddle():
            data = update.callback_query.data
            if data in ["Next riddle", "Back"]:
                machine.next_riddle(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: riddle question delete""\033[m")

        elif machine.is_question_music():
            data = update.callback_query.data
            if data in ["Suggestion from bot", "Search yourself"]:
                machine.music_reply(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: music question delete""\033[m")

        elif machine.is_question_mood_suggest():
            data = update.callback_query.data
            if data in ["Happy", "Angry", "Sad", "Depressed", "Homesick", "Tired", "Bored", "Stressed"]:
                machine.suggest_mood_music(update)
                machine.suggest_next_music(update) # jump directly
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: mood question delete""\033[m")

        elif machine.is_suggest_next():
            data = update.callback_query.data
            if data in ["Suggestion from bot again", "Back"]:
                machine.next_suggest(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: suggest next delete""\033[m") 

        elif machine.is_happy_result():
            data = update.callback_query.data
            if data in ["No, search again.", "Yes, got it."]:
                machine.search_next(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: happy result delete""\033[m")

        elif machine.is_question_mood_chat():
            data = update.callback_query.data
            if data in ["開心", "生氣", "難過", "沮喪", "疲累", "無聊", "有壓力"]:
                machine.msg = machine.msg.edit_text("Waiting for sending picture...", reply_markup=None)
                machine.mood = update.callback_query.data
                pic_name = "./img/" + update.callback_query.data + str(random.randrange(1,3)) + ".png"
                photo = open(pic_name, "rb")
                bot.send_photo(chat_id=update.callback_query.message.chat.id, photo=photo)
                photo.close()
                machine.msg = machine.msg.edit_text("Hope this picture can let you be more happy😙")
                machine.chat_with_mood(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: chat mood delete""\033[m")

        elif machine.is_give_pic_or_text():
            data = update.callback_query.data
            if data in ["有", "沒有"]:
                machine.mood_be_better(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: chat better delete""\033[m")

        elif machine.is_question_better():
            data = update.callback_query.data
            if data in ["Chat again", "Back"]:
                machine.next_chat(update)
            else:
                update.callback_query.message.edit_reply_markup(reply_markup=None)
                print("\033[0;32;31m""error: chat again delete""\033[m")

        else:
            update.callback_query.message.edit_reply_markup(reply_markup=None)
            print("\033[0;32;31m""error: input delete""\033[m")

    else:
        if update.message.text == "/restart":
            init(update, machine)
            return "ok"
        elif update.message.text == "/superadmin":
            user_text = [people+"\n" for people in machine.user_list]
            user_text = "User:"
            for people in machine.user_list:
                user_text = user_text + "\n" + people
            
            user_text  = user_text + "\nToken:"
            for tok in machine.be_token:
                user_text = user_text + "\n" + tok
            update.message.reply_text(user_text)
            return "ok"
            
        if machine.is_start():
            if update.callback_query != None:
                print("\033[0;32;31m""Error if""\033[m")
            else:
                if update.message.text == "/start":
                    machine.start_msg(update)
                else:
                    update.message.reply_text("Please enter 👉 /start to start interaction with me ✌🏻")
        elif machine.is_riddle():
            machine.riddle_to_answer(update)
            machine.answer_riddle_to_question(update) # jump directly
        elif machine.is_search():
            machine.search_result_and_question(update)
            machine.question_result(update) # jump directly
        elif machine.is_chat_deeply() and machine.chat_times <= 1:
            machine.chat_times = machine.chat_times + 1
            machine.chat_deeply(update)
        elif machine.chat_times >= 2:
            machine.be_token.append(update.message.text)
            update.message.reply_text("Hope you have good time today")
            machine.to_start(update)
        else:
            print("\033[0;32;31m""Abort user input""\033[m")

    return "ok"

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

def start(bot, update):
    update.message.reply_text("Good job")

if __name__ == "__main__":
    _set_webhook()
    app.run(port=5000)


