# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:25:39 2015

@author: isman7
"""

import requests

getMe = u'getMe'
getUpdates = u'getUpdates'

class chat(object):
    
    def getID(self):
        return self.id
    
    def __init___(self):
        self.id = 0
        
        
class user(chat):

    def json(self):
        
        userjson = {'id': self.id,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'username': self.username
                    }  
        
        return userjson
    
    def __init__(self, userJson):
        chat.__init__(self)
        self.json = userJson
        self.id = self.json['id']
        try:         
            self.first_name = self.json['first_name']
            self.last_name = self.json['last_name']
            self.username = self.json['username']
        except KeyError, e:
            print e    

class message(object):
    
    def __init__(self, update):
        
        try:
            
            self.json = update['message'] 
        except KeyError, e:
            print e
            return None          
            
        self.date = self.json['date']
        self.text = self.json['text']
        self.userFrom = user(self.json['from'])
        self.message_id = self.json['message_id']
        self.chat = (self.json['chat'])
        
            
            
class bot(object):
    
    def sendMessage(self, chat_id, text, ): 
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