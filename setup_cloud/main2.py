#!/usr/bin/python
import atexit
import ConfigParser
import signal
import sys
import time
import pyupm_grove as grove
import pyupm_grovespeaker as upmGrovespeaker
import pyupm_i2clcd as lcd
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from wit import Wit
import os

credentials = ConfigParser.ConfigParser()
credentialsfile = "credentials.config"
credentials.read(credentialsfile)

button = grove.GroveButton(8)
display = lcd.Jhd1313m1(0, 0x3E, 0x62)
light = grove.GroveLight(0)
light1 = grove.GroveLight(0)
light2 = grove.GroveLight(1)
light3 = grove.GroveLight(2)
light4 = grove.GroveLight(3)
relay = grove.GroveRelay(2)

def functionLight(bot, update):
    # luxes = light.value()
    # if luxes == 0:
    #     output_msg  = "NO hay estacionamiento"
    # else:
    #     output_msg  = "SI hay estacionamiento"
    # bot.sendMessage(update.message.chat_id, text=output_msg)
    # os.system("curl ")
    lux_lights = [light1,light2,light3,light4]
    i=0
    valid_lux=0
    for x in lux_lights:
        i+=1
        luxes = x.value()
        if luxes == 0:
            output_msg  = "Lugar #" + str(i) + " - OCUPADO"
        else:
            output_msg  = "Lugar #" + str(i) + " - LIBRE"
            if valid_lux == 0:
                valid_lux = i
        bot.sendMessage(update.message.chat_id, text=output_msg)
    os.system("curl http://172.99.106.216:9000/sensor?value=" + str(valid_lux))

def functionMessage(bot, update):
    bot.sendMessage(update.message.chat_id, text=message)

def functionRelay(bot, update):
    relay.on()
    time.sleep(2)
    relay.off()
    bot.sendMessage(update.message.chat_id, text='Relay Used!')


def functionEcho(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def SIGINTHandler(signum, frame):
    raise SystemExit

def exitHandler():
    print "Exiting"
    sys.exit(0)

atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

if __name__ == '__main__':
    credential = credentials.get("telegram", "token")
    updater = Updater(credential)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("light", functionLight))
    dp.add_handler(CommandHandler("message", functionMessage))
    dp.add_handler(CommandHandler("relay", functionRelay))
    dp.add_handler(MessageHandler([Filters.text], functionEcho))
    updater.start_polling()
    message = "Hi! I'm Main!"

    while True:
        luxes = light.value()
        luxes = int(luxes)
        display.setColor(luxes, luxes, luxes)
        display.clear()

        if button.value() is 1:
            display.setColor(255, 0, 0)
            display.setCursor(0,0)
            display.write(str(message))
            relay.on()
            time.sleep(1)
            relay.off()

updater.idle()

