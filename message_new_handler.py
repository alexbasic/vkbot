import datetime
import random

class MessageNewHandler:
    def __init__(self, vk):
        self.vk = vk
    
    def handle(self, event):
        request_text = event['object']['text']
        print("==>responce")
        reply = self.get_reply(request_text)
        max_int = 2147483647
        random_id = random.randint(0, max_int)
        user_id = event['object']['from_id']
        resp = self.write_msg(user_id, reply, random_id)
        print(datetime.datetime.now().isoformat(), 'send message result =', resp.text)
    
    def write_msg(self, user_id, message, random_id):
        return self.vk.vk_method_get('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})
        
    def get_reply(self, request):
        if request == "привет":
            return "Хай."
        elif request == "пока":
            return "До встречи."
        else:
            return "Неизвестная команда."
