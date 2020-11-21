import os
from flask import Flask, request
import telebot


TOKEN = '1423141786:AAFGYwvJG9LaJRQD-uiVbd1-iwRqmLKw0eI'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def start(message):
    res = '/courses - список курсов \n' \
          '/schedule - расписание курсов\n' \
          '/planning - список курсовв котрые ведется набор,'
    bot.reply_to(message, res)


@bot.message_handler(commands=['courses'])
def echo_message(message):
    res = 'Ухты'
    bot.reply_to(message, res)


@bot.message_handler(commands=['schedule'])
def echo_message(message):
    res = 'Ухты пухты'
    bot.reply_to(message, res)


@bot.message_handler(commands=['planning'])
def echo_message(message):
    res = 'Ура'
    bot.reply_to(message, res)


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
