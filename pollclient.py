import datetime
import requests
import json
import os
import random
from vk import Vk
from tools import EventProcessor
from message_new_handler import MessageNewHandler

#config

access_token = os.environ.get('access_token', '')
group_id = int(os.environ.get('group_id', 0))

vk = Vk(access_token)
event_processor = EventProcessor(group_id)
message_new_handler = MessageNewHandler(vk)

@event_processor.message_new()
def message_new_handler_fn(event):
    message_new_handler.handle(event)
    return "ok", 200

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
    for update in event['updates']:
        try:
            event_processor.process(update)
        except Exception:
            print("Error of update process")
