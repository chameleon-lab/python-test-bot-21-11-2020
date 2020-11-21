import os
from flask import Flask, request
import telebot
import json


TOKEN = '1423141786:AAFGYwvJG9LaJRQD-uiVbd1-iwRqmLKw0eI'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def start(message):
    res = '/courses - список курсов \n' \
          '/planning - расписание запуска курсов,'
    bot.reply_to(message, res)


@bot.message_handler(commands=['courses'])
def echo_message(message):
    with open('courses.txt') as file:
        courses = [item.split(',') for item in file]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for text, url in courses:
        url_button = telebot.types.InlineKeyboardButton(text=text, url=url.strip(' \n'))
        keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Выбери курс", reply_markup=keyboard)


def echo_message(message):
    with open('planning.json', encoding="utf8") as json_file:
        data = json.load(json_file)
    res = ''
    for item in data['courses']:
        res += f"<b>{item['course']}</b>\n" \
                   f"<i>Online:</i> <code>{item['schedule']['online']}</code>\n" \
                   f"<i>Offline:</i> <code>{item['schedule']['offline']}</code>\n"
    bot.send_message(message.from_user.id, text=res, parse_mode='HTML')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://python-test-bot-21-11-2020.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
