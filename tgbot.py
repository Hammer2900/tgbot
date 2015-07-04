# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:25:39 2015

@author: isman7
"""

import requests

getMe = u'getMe'
getUpdates = u'getUpdates'

class Chat(object):
    
    def json(self):
        return self.__dict__  
    
    def __init__(self):
        self.id = 0
        
        
class User(Chat):

    def __init__(self, **kwargs):
        Chat.__init__(self)
        try:
            self.__dict__ = kwargs['UserJson']
        except KeyError, e:
            print e                
            self.id = 0
            self.first_name = u''
            self.last_name = u''
            self.username = u''

class GroupChat(Chat):
    
    def __init__(self, **kwargs):
        Chat.__init__(self)
        try:
            self.__dict__ = kwargs['GroupJson']
        except KeyError, e:
            print e                
            self.id = 0
            self.title = u''

class Message(object):
    
    def __init__(self, **kwargs):
        
        try:
            update = kwargs['Update'] 
            self.__dict__ = update['message']            
            self.userFrom = User(UserJson = self.__dict__['from'])
            if 'first_name' in self.chat:
                self.chat = User(UserJson = self.chat)
            elif 'title' in self.chat:
                self.chat = GroupChat(GroupJson = self.chat)
            else: 
                self.chat = Chat()
        except KeyError, e:
            print e
            self.date = 0
            self.text = u''
            self.userFrom = User()
            self.chatTo = Chat()
            self.message_id = u''
            self.chat = Chat()
            
class bot(object):
    
    def sendMessage(self, chat_id, text): 
        print chat_id
        return requests.get(self.url + u'sendMessage?chat_id=' + unicode(chat_id) + u'&text=' + text)
    
    def getUpdate(self):
    
        try:        
            self.lastUpdates = requests.get(self.url + getUpdates + u'?offset=' + unicode(self.lastUpdateID + 1))
            self.lastUpdateID = self.lastUpdates.json()['result'][-1]['update_id']
            self.updatesBuff = self.updatesBuff + self.lastUpdates.json()['result']        
        except KeyError, e:
            print str(e)
        except IndexError, e:
            print str(e)
        
        try: 
            nextUpdate = self.updatesBuff[0]         
            self.updatesBuff = self.updatesBuff[1:]
            return nextUpdate
        except IndexError, e:
            print str(e)
            return None

    def __init__(self, path_to_key):
        
        keyFile = open(path_to_key, 'r')
        self.botKey = keyFile.readline().split('\n')[0]
        self.url = u'https://api.telegram.org/bot' + unicode(self.botKey) + u'/'
        self.getMe = requests.get(self.url + getMe)
        
        # TODO evaluate response to getMe. 
        
        self.lastUpdates = requests.get(self.url+getUpdates)
        
        try:        
            self.lastUpdateID = self.lastUpdates.json()['result'][-1]['update_id']
            self.updatesBuff = self.lastUpdates.json()['result']  
        except KeyError, e:
            print 'A KeyError ocurred'
            print str(e)
        except IndexError, e:
            self.lastUpdateID = 0
            self.updatesBuff = []
            print e
            return None

        keyFile.close()