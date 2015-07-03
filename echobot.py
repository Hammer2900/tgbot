# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 01:22:20 2015

@author: isman7
"""

import tgbot

echobot = tgbot.bot('ismansiete.txt')

while True: 
    update = echobot.getUpdate()    
    if update:
        message = tgbot.message(update)
        userFrom = message.userFrom
        echobot.sendMessage(userFrom.id, message.text)       
        

    
    