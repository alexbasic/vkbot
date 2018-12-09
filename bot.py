import datetime
import requests
import json

#config

api_version = '5.92'
access_token = None
group_id = None

with open('config.json') as json_config:
    config = json.load(json_config)
    access_token = config["access_token"]
    group_id = config["group_id"]
    
exit()

#vk_api

root_url = 'https://api.vk.com/method'

def join_url_params(params):
    result = None
    for k, v in params.items():
        if (result == None):
            result = "{1}={2}".format(result, k, v)
        else:
            result = "{0}&{1}={2}".format(result, k, v)
    return result

def vk_method_get(name, params):
    url_params = ''
    if (params == None or params == {}):
        url_params = "access_token={1}&v={2}".format(access_token, api_version)
    else:
        url_params = join_url_params(params)
        url_params = "{0}&access_token={1}&v={2}".format(url_params, access_token, api_version)
    url = "{0}/{1}?{2}".format(root_url, name, url_params)
    response = requests.get(url)
    if (response.status_code != 200):
	    raise Exception('Network error. Status: {0}'.format(response.status_code))
    return response
    
def vk_longpoll_listen(server, key, ts):
    longpoll_wait = 25
    url = "{0}?act=a_check&key={1}&ts={2}&wait={3}".format(server, key, ts, longpoll_wait)
    print('LongPollConnect=', url)
    response = requests.get(url)
    if (response.status_code != 200):
	    raise Exception('Poll error. Status: {0}. Message: {1}'.format(response.status_code))
    return response
    
#botlib

def write_msg(user_id, message, random_id):
    return vk_method_get('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})

#main

try:
    raise Exception("ta-da")
except Exception as e:
    import traceback
    print("Exception: ", traceback.format_exc())
exit()

result = vk_method_get('groups.getLongPollServer', {'group_id': group_id}).json()
print('GetLongPollServer=', result)
server = result['response']['server']
key = result['response']['key']
ts = result['response']['ts']

while True:    
    event = vk_longpoll_listen(server, key, ts).json()
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
                
