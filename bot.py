import datetime
import requests
import json
import os
from vk import Vk

#config

access_token = os.environ.get('access_token', '')
group_id = os.environ.get('group_id', '')

vk = Vk(access_token)
    
#botlib

def write_msg(user_id, message, random_id):
    return vk.vk_method_get('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})

#main
result = vk.vk_method_get('groups.getLongPollServer', {'group_id': group_id}).json()
if Vk.IsError(result):
    print (result)
    exit(-1)
print('GetLongPollServer=', result)
server = result['response']['server']
key = result['response']['key']
ts = result['response']['ts']

while True:    
    event = vk.vk_longpoll_listen(server, key, ts).json()
    print(datetime.datetime.now().isoformat(), ' vk_longpoll_listen_as_json=', event)
    ts = event['ts']
    if len(event['updates'])<1: continue
    update = event['updates'][0]
    if update['type'] == 'message_new':
        if update['group_id'] == group_id:
            request = update['object']['text']
            if request == "привет":
                resp = write_msg(update['object']['from_id'], "Хай.", random_id)
                print(datetime.datetime.now().isoformat(), 'send message result =', resp.text)
            elif request == "пока":
                resp = write_msg(update['object']['from_id'], "До встречи.", random_id)
                print(datetime.datetime.now().isoformat(), 'send message result =', resp.text)
            else:
                resp = write_msg(update['object']['from_id'], "Неизвестная команда.", random_id)
                print(datetime.datetime.now().isoformat(), 'send message result =', resp.text)
        else:
            print("Skip message")
                
