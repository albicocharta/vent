#!/usr/bin/env python
# pylint: disable=wrong-import-position
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
password = {
    'adm' : 'password_adm',
    'horeog' : 'password_horeog',
    'zvuk' : 'password_zvuk',
    'view' : 'password_view',
    'auto' : 'password_auto',
    'horeog_start' : 'password_horeog_start'
    }

horogstoptime = ''


import os
from datetime import datetime
import asyncio
import subprocess
from sys import argv

import logging
from typing import NoReturn

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Bot
from telegram.error import Forbidden, NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# В key_arr 7 значений.  0 позиция отведена под программу, которая находится в avto.py , остальные 1..6  это релюшки .

key_dict = {'зрительный':1, 'торжественный':2, 'гостиная':3, 'администрация':4, 'студия':5, 'приточка':6 }

key_arr = [False]*(len(key_dict) + 1)

horogstoptime = ''

# эта строчка нужна что бы можно было запускать бот с включенным расписанием timestack() .
if len(argv) != 1:
    key_arr[0] = True


def key_arr_0(bool):
    key_arr[0] = bool
    

def key_arr_of_read_system():
	bashCommand = "usbrelay"
	process =  subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
    
	output = output.split()
	#print('output',output)
	for i in range(1,7):
		if ('HW554_' + str(i) + '=1').encode('UTF-8') in output:
			key_arr[i] =  True
			#print('True ', i)
		elif ('HW554_' + str(i) + '=0').encode('UTF-8') in output:
			key_arr[i] =  False
			#print('False ', i)
		else:
			print('Error: команда Вопрос ',i)
    
    #print('read')
    
def startvent (i):
    key_arr[i] =  True
    s = 'HW554_' + str(i) + '=1'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)
   
   
def stopvent (i):
    key_arr[i] =  False
    s = 'HW554_' + str(i) + '=0'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)
    
    
def ventview():

    key_arr_of_read_system()

    f = open('/var/vent/auto.txt', 'r')
    if f.read().split('\n')[0] == 'True':
        key_arr[0] = True
    else:
        key_arr[0] = False
    f.close()
    if key_arr[0] :
        s = 'ПРОГРАММА, '
    else:
        s ='программа, '

    for i in key_dict.keys():
        if key_arr[key_dict[i]] :
            s += i.upper() + ', '
        else:
            s += i + ', '
    return s
    
    
def timeview():
    datetimenow = datetime.now()
    time = datetimenow.strftime('%H:%M')
    return str(time)





async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    
    async with Bot("TOKEN_TELEGRAM") as bot:   
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.
        try:
            update_id = (await bot.get_updates())[0].update_id
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        while True:
            try:
                update_id = await echo(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1


async def echo(bot: Bot, update_id: int) -> int:
    """Echo the message the user sent."""
    global horogstoptime
    # Request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1

        # your bot can receive updates without messages
        # and not all messages contain text
        
        if update.message and update.message.text:
            # Reply to the message
            logger.info("Found message %s!", update.message.text)
            
            key_arr_of_read_system()
            
            massage = update.message.text
            massage = massage.lower() # в нижний регистр
            massage = massage.split() # list
            
            if massage[0] == password['view'] :
                 await update.message.reply_text(ventview())
                 
            elif massage[0] == password['adm'] :
                horogstoptime = ''
                for i in key_dict.keys():
                    if i in massage :
                        startvent(key_dict[i])
                    else:
                        stopvent(key_dict[i])
                await update.message.reply_text(ventview())
                
            elif massage[0] == password['horeog'] :
                if key_arr[6]:
                    stopvent(6)
                   # horogstoptime = '\n16:55' 
                    horogstoptime = '\n'+ str(int(timeview()[0:2]) + 2).zfill(2) + timeview()[2:]
                   # os.system('python3 /root/scripts/sleep6.py')
                   # subprocess.call(['python3','/root/scripts/sleep6.py'])
                    f = open('/var/vent/horeog.txt', 'a')
                    f.write(horogstoptime)
                    f.close()
                    s_horeog = 'Приточка остановлена. Она включится в ' + horogstoptime + ' .'
                    await update.message.reply_text( s_horeog )
                    #await asyncio.sleep(2*60*60)
                    #await startvent(6)
                    #await update.message.reply_text( 'Приточка  включена' )
                else:
                    await update.message.reply_text('Приточка уже отключена')
                    
            elif massage[0] == password['zvuk']:
                if 'вкл' in massage:
                    startvent(5)
                    await update.message.reply_text('Вкл')
                else:
                    stopvent(5)
                    await update.message.reply_text('Откл')
                    
            elif massage[0] == password['auto']:
                f = open('/var/vent/auto.txt', 'r')
                a = f.read().split('\n')
                f.close()
                    
                if 'вкл' in massage:
                    a[0] = 'True' 
                    f = open('/var/vent/auto.txt', 'w')
                    a = '\n'.join(a)
                    f.write(a)
                    f.close()
                    await update.message.reply_text(ventview())
                elif 'откл' in massage:
                    a[0] = 'False' 
                    f = open('/var/vent/auto.txt', 'w')
                    a = '\n'.join(a)
                    f.write(a)
                    f.close()
                    await update.message.reply_text(ventview())
                else:
                    await update.message.reply_text('\n'.join(a))
            elif massage[0] == password['horeog_start']:
                if key_arr[6]:
                    await update.message.reply_text('Приточка уже включена.')
                else:
                    startvent(6)
                    await update.message.reply_text('Приточка включена.')

                    
                                   
            else:
                await update.message.reply_text('Некорректная команда.' )
            
        return next_update_id
    return update_id


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
