
class UnexpectedEventException(Exception):
    pass

class EventProcessor:
    def __init__(self, group_id, need_secret = False, secret = None):
        self._group_id = group_id
        self.need_secret = need_secret
        self.secret = secret
        
    def process(self, event):
        group_id = event['group_id']
        event_type = event['type']
        if self.need_secret:
            self.verify_secret(remote_secret= event['secret'] , my_secret= self.secret)
        if (group_id != self._group_id):
            raise Exception("not supported group_id: {0}".format(group_id))
        if (event_type == "confirmation"):
            result = self._confirmation_fn(event)
            return result
        if (event_type == "message_new"):
            return self._message_new_fn(event)
        return self._error_fn(UnexpectedEventException("Unexpected event: ", event))
    
    def verify_secret(self, remote_secret, my_secret):
        if my_secret == None: raise Exception("Need to set secret in config")
        if my_secret != remote_secret: raise Exception("Wrong secret")
    
    def error(self):
        def decorator(f):
            self._error_fn = f
            return f
        return decorator
    
    def confirmation(self):
        def decorator(f):
            self._confirmation_fn = f
            return f
        return decorator
    
    def message_new(self):
        def decorator(f):
            self._message_new_fn = f
            return f
        return decorator
