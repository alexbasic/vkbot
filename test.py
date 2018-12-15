from tools import EventProcessor
import unittest
from message_new_handler import MessageNewHandler
import types

class EventProcessorTest(unittest.TestCase):
    def setUp(self):
        self.group_id = 123
        self.event_processor = EventProcessor(self.group_id)

    #def tearDown(self):
    #    pass
        
    def test_must_confirm(self):
        data = {"type": "confirmation", "group_id": self.group_id, "object": None}
        expected = data
        actual = None
        @self.event_processor.confirmation()
        def confirm_handler(event):
            nonlocal actual
            actual = event
        self.event_processor.process(data)
        self.assertEqual(actual, expected)
        
    def test_message_new(self):
        data = {"type": "message_new", "group_id": self.group_id, "object": None}
        expected = data
        actual = None
        @self.event_processor.message_new()
        def message_new_handler(event):
            nonlocal actual
            actual = event
        self.event_processor.process(data)
        self.assertEqual(actual, expected)

class VkStub:
    result = None
    def __init__(self, response):
        self.response = response
    def vk_method_get(self, message_type, value):
        Test_response = type('TestResponse', (), {"text": self.response})
        self.result = Test_response()
        return self.result

class MessageNewHandlerTest(unittest.TestCase):
    def setUp(self):
        self.message_send_response_stub = '{"response":35}'
        self.vk_stub = VkStub(self.message_send_response_stub)
        self.message_new_handler = MessageNewHandler(self.vk_stub)

    #def tearDown(self):
    #    pass
        
    def test_must_handle(self):
        event = {"type": "message_new", "group_id": 123, "object": {"text": "test text", "from_id": 10}}
        self.message_new_handler.handle(event)
        self.assertEqual(self.vk_stub.result.text, self.message_send_response_stub)
        

if __name__ == '__main__':
    unittest.main()
