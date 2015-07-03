# tgbot
Library for quick Telegram Bot with Python. 

## Example of use

``` 
import tgbot
bot = tgbot.tgbot('path_to_key_file')
last_update = bot.getUpdate() #Gets JSON object that corresponds to last-non-processed update. 
bot.sendMessage(chat_id, text) #Sends a message to a group or a person.

``` 

