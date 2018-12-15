class EventProcessor:
    def __init__(self, group_id):
        self._group_id = group_id
        
    def process(self, event):
        group_id = event['group_id']
        event_type = event['type']
        if (group_id != self._group_id):
            raise Exception("not supported group_id: {0}".format(group_id))
        if (event_type == "confirmation"):
            self._confirmation_fn(event)
        if (event_type == "message_new"):
            self._message_new_fn(event)
    
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
