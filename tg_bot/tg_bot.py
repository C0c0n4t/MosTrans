import telebot
from telebot import types
from global_variables import BOT_TOKEN, URL
import api
import sys
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет, я бот для проверки телеграмм webapps!)', reply_markup=webAppKeyboard()) 

@bot.message_handler(content_types=['text'])
def handle_text(message):
    response = api.get_info(message.text)
    bot.reply_to(message, response)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    audio_file = bot.download_file(file_info.file_path)
    # bot.send_audio(message.chat.id, audio=audio_file)
    # bot.send_message(message.chat.id, message)
    bot.reply_to(message, speech_to_text(audio_file))

def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
   keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo("https://www.wikipedia.org/") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Веб-интерфейс", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру

bot.infinity_polling()