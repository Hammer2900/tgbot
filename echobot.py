# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 01:22:20 2015

@author: isman7
"""

import tgbot

echoBot = tgbot.bot('ismansiete.txt')

while True: 
    updateBot = echoBot.getUpdate()    
    if updateBot:
        message = tgbot.message(update=updateBot)
        userFrom = message.userFrom
        echoBot.sendMessage(userFrom.id, message.text)       
        

    
    