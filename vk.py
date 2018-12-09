import datetime
import requests
import json
    
class Vk(object):

    _root_url = 'https://api.vk.com/method'
    _api_version = '5.92'
    _access_token = None
    _longpoll_wait = 25
    
    def __init__(self, access_token):
        self._access_token = access_token
    
    @staticmethod
    def IsError(response):
        return (response == None or "error" in response.keys())
    
    def vk_method_get(self, name, params):
        url_params = ""
        if (params == None or params == {}):
            url_params = "access_token={1}&v={2}".format(self._access_token, self._api_version)
        else:
            url_params = self.join_url_params(params)
            url_params = "{0}&access_token={1}&v={2}".format(url_params, self._access_token, self._api_version)
        url = "{0}/{1}?{2}".format(self._root_url, name, url_params)
        response = requests.get(url)
        if (response.status_code != 200):
	        raise Exception('Network error. Status: {0}'.format(response.status_code))
        return response
    
    def vk_longpoll_listen(self, server, key, ts):
        url = "{0}?act=a_check&key={1}&ts={2}&wait={3}".format(server, key, ts, self._longpoll_wait)
        response = requests.get(url)
        if (response.status_code != 200):
	        raise Exception('Poll error. Status: {0}. Message: {1}'.format(response.status_code))
        return response
    
    def join_url_params(self, params):
        result = None
        for k, v in params.items():
            if (result == None):
                result = "{1}={2}".format(result, k, v)
            else:
                result = "{0}&{1}={2}".format(result, k, v)
        return result
    
