import os
from flask import Flask, request
from tools import EventProcessor
from message_new_handler import MessageNewHandler
from vk import Vk
#import logging

access_token = os.environ.get('access_token', '')
group_id = int(os.environ.get('group_id', 0))
server_confirmation_key = os.environ.get('server_confirmation_key', None)
secret = os.environ.get('secret', '')

server = Flask(__name__)
event_processor = EventProcessor(group_id, True, secret)
vk = Vk(access_token)
message_new_handler = MessageNewHandler(vk)

@event_processor.confirmation()
def confirm_handler_fn(event):
    if server_confirmation_key == None:
        raise Exception("server confirmation key is not set")
    return server_confirmation_key
    
@event_processor.message_new()
def message_new_handler_fn(event):
    message_new_handler.handle(event)
    return "ok"

@event_processor.error()
def error_handler_fn(error):
    #print(error)
    server.logger.warning(error)
    return "ok"

@server.route("/vkhook", methods = ['POST'])
def webhook():
    if (not request.is_json): raise Exception("request is not json")
    content = request.get_json()
    result = event_processor.process(content)
    return result, 200

#server.logger.setLevel(logging.CRITICAL)
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
