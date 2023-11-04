import os
import telebot
from datetime import datetime
import http.client
import json

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AEMET_TOKEN = os.environ.get('AEMET_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

sQLite=[]

# Wellcome Message 
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "ChatBot Running at "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# Drop data
@bot.message_handler(commands=['drop'])
def drop(message):
    sent_msg = bot.send_message(message.chat.id, "What do I drop?" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,drop_handler)

def drop_handler(message):
    sQLite.append(message.text)
    bot.send_message(message.chat.id, "Saved in position " + str(len(sQLite)))

# Pop data
@bot.message_handler(commands=['pop'])
def pop(message):
    if len(sQLite) == 0:
        bot.send_message(message.chat.id, "Cannot pop from empty stack")
    else:
        bot.send_message(message.chat.id, "Pop from position "+ str(len(sQLite)) + ": " + sQLite.pop(len(sQLite)-1))

# Sends the last whether report from Valladolid
@bot.message_handler(commands=['whether'])
def whether(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata//api/observacion/convencional/datos/estacion/2422?api_key="+AEMET_TOKEN, headers=headers)

    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", entrada1['datos'][25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    entrada2=json.loads(data2.decode("utf-8"))[0]
    bot.send_message(message.chat.id, "*Location: *" + entrada2['ubi'] + "\n*Date of Data:* " 
    + entrada2['fint'] + "\n*Temperature:* " + str(entrada2['ta']) + "ºC\n*Humidity:* " + str(entrada2['hr']) +
    "%\n*Accumulated Precipitation:* " + str(entrada2['prec']) + "l/m^2\n*Average Wind Speed:* " + str(entrada2['vvu']) + 
    "m/s\n*Pressure:* " + str(entrada2['pres']) + "hPa\n*Visibility:* " + str(entrada2['vis']) + "Km", parse_mode= 'Markdown')

# Sends the last radar image from Palencia (closest to Valladolid)
@bot.message_handler(commands=['radar'])
def radar(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/red/radar/regional/vd?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_photo(message.chat.id,data2)



# Add two numbers 
@bot.message_handler(commands=['sum'])
def send_sum(message):
    sent_msg = bot.send_message(message.chat.id, "What numbers do I add?:\n\n Num 1:" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,sum_handler)

def sum_handler(message):
    num1=message.text
    sent_msg = bot.send_message(message.chat.id, "Num 2:" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, sum_handler2, num1)

def sum_handler2(message,num1):
    num2=message.text
    num=int(num1)+int(num2)
    bot.send_message(message.chat.id,"Sum is " + num1 + "+" + num2 + " = " + str(num))

# Last resort
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Ni idea que me dices illo")

bot.infinity_polling()