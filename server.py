import os
from flask import Flask, request
from tools import EventProcessor
from message_new_handler import MessageNewHandler
from vk import Vk
#import logging

access_token = os.environ.get('access_token', '')
group_id = int(os.environ.get('group_id', 0))
server_confirmation_key = os.environ.get('server_confirmation_key', '')

server = Flask(__name__)
event_processor = EventProcessor(group_id)
vk = Vk(access_token)
message_new_handler = MessageNewHandler(vk)

@event_processor.confirmation()
def confirm_handler_fn(event):
    #nonlocal server_confirmation_key
    return server_confirmation_key, 200
    
@event_processor.message_new()
def message_new_handler_fn(event):
    #nonlocal message_new_handler
    message_new_handler.handle(event)
    return "ok", 200

@server.route("/vkhook", methods = ['POST'])
def webhook():
    #nonlocal event_processor
    if (not request.is_json): raise Exception("request is not json")
    content = request.get_json()
    event_processor.Process(content)
    return "ok", 200

#server.logger.setLevel(logging.CRITICAL)
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
