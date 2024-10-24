import os
import telebot
from datetime import datetime
import http.client
import json

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AEMET_TOKEN = os.environ.get('AEMET_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Wellcome Message 
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "ChatBot Running at "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# Enviar el ultimo informe de una estacion
@bot.message_handler(commands=['observacion_estacion'])
def observacion_estacion_pedida(message):
    sent_msg = bot.send_message(message.chat.id, "¿De qué estación quiere la información? _Valladolid=2422_" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,observacion_estacion_devolucion)

def observacion_estacion_devolucion(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata//api/observacion/convencional/datos/estacion/"+message.text+"?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    
    conn.request("GET", entrada1['datos'][25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    entrada2=json.loads(data2.decode("utf-8"))[0]

    conn.request("GET", entrada1['metadatos'][25:200], headers=headers)
    res3 = conn.getresponse()
    data3 = res3.read()
    entrada3=json.loads(data3.decode("windows-1250","ignore"))
    #print(entrada3['campos'][0])
    salida = ""
    for i in entrada2:
        for j in entrada3['campos']:
            if j['id']==i:
                bot.send_message(message.chat.id, j['descripcion']+":\n"+str(entrada2[i]))
    

# Sends the last radar image from Palencia
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

@bot.message_handler(commands=['presion'])
def presion(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/mapasygraficos/analisis/?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_photo(message.chat.id,data2)

@bot.message_handler(commands=['rayos'])
def rayos(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/red/rayos/mapa/?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_photo(message.chat.id,data2)

@bot.message_handler(commands=['incendios'])
def incendios(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/incendios/mapasriesgo/estimado/area/p/?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_photo(message.chat.id,data2)

@bot.message_handler(commands=['prediccion_hoy'])
def prediccion_hoy(message):
    sent_msg = bot.send_message(message.chat.id, "¿De qué provincia quiere la información? _Valladolid=47_" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,prediccion_hoy_devolucion)

def prediccion_hoy_devolucion(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/prediccion/provincia/hoy/"+message.text+"?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_message(message.chat.id, data2.decode("windows-1250","ignore"))

@bot.message_handler(commands=['prediccion_manana'])
def prediccion_manana(message):
    sent_msg = bot.send_message(message.chat.id, "¿De qué provincia quiere la información? _Valladolid=47_" ,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,prediccion_manana_devolucion)

def prediccion_manana_devolucion(message):
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    conn.request("GET", "/opendata/api/prediccion/provincia/manana/"+message.text+"?api_key="+AEMET_TOKEN, headers=headers)
    res = conn.getresponse()
    data = res.read()
    entrada1=json.loads(data.decode("utf-8"))
    conn.request("GET", str(entrada1['datos'])[25:100], headers=headers)
    res2 = conn.getresponse()
    data2 = res2.read()
    bot.send_message(message.chat.id, data2.decode("windows-1250","ignore"))


# Last resort
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Unregistered command")




bot.infinity_polling()
