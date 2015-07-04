# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:25:39 2015

@author: isman7
"""

import requests


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
        except KeyError:
            self.id = 0
            self.first_name = u''
            self.last_name = u''
            self.username = u''

class GroupChat(Chat):
    
    def __init__(self, **kwargs):
        Chat.__init__(self)
        try:
            self.__dict__ = kwargs['GroupJson']
        except KeyError:
            self.id = 0
            self.title = u''

class Message(object):
    
    def json(self):
        jsonDict = self.__dict__
        for attribute, value in jsonDict.iteritems(): 
            try: 
                jsonDict[attribute] = value.json()
            except TypeError:
                pass
            except AttributeError:
                pass
        return jsonDict     
    
    
    def __init__(self, **kwargs):
        try:
            if 'Update' in kwargs:            
                update = kwargs['Update'] 
                self.__dict__ = update.message            
            elif 'result' in kwargs:
                self.__dict__ = kwargs['result'].json()['result']
            self.userFrom = User(UserJson = self.__dict__['from'])
            if 'first_name' in self.chat:
                self.chat = User(UserJson = self.chat)
            elif 'title' in self.chat:
                self.chat = GroupChat(GroupJson = self.chat)
            else: 
                self.chat = Chat()
        except KeyError:
            self.date = 0
            self.userFrom = User()
            self.message_id = 0
            self.chat = Chat()
            #Optionals:
            self.text = u''
            #Extras:
            self.chatTo = Chat()
            
class Update(object):
    
    def __init__(self, **kwargs):
        try:
            self.__dict__ = kwargs['UpdateJson']
        except KeyError:
            pass
            
class bot(object):
    
    def sendMessage(self, **kwargs): 
        
        try: 
            message = requests.get(self.url + u'sendMessage?chat_id=' + unicode(kwargs['chat_id']) + u'&text=' + kwargs['text'])
            return Message(result = message)
        except KeyError:
            return None
        
    def getMe(self):
        return requests.get(self.url + u'getMe')        
    
    def getUpdates(self):
        try:        
            self.lastUpdates = requests.get(self.url + u'getUpdates?offset=' + unicode(self.lastUpdateID + 1))
            self.lastUpdateID = self.lastUpdates.json()['result'][-1]['update_id']
            self.updatesBuff = self.updatesBuff + self.lastUpdates.json()['result']        
            return self.lastUpdates
        except KeyError, e:
            print str(e)
        except IndexError:
            return None
        
    def getUpdate(self):
        self.getUpdates()
        try: 
            nextUpdate = self.updatesBuff[0]         
            self.updatesBuff = self.updatesBuff[1:]
            update = Update(UpdateJson=nextUpdate)
            return update
        except IndexError:
            return None

    def __init__(self, path_to_key):
        
        keyFile = open(path_to_key, 'r')
        self.botKey = keyFile.readline().split('\n')[0]
        self.url = u'https://api.telegram.org/bot' + unicode(self.botKey) + u'/'
        self.updatesBuff = []
        self.lastUpdateID = 0
        self.lastUpdates = self.getUpdates()
        
        keyFile.close()