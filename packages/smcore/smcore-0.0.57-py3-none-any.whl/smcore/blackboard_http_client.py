import json
import requests
from google.protobuf import json_format

from . import types_pb2 as pb2


class BlackboardHTTPClient:
    def __init__(self, addr):
        # instantiate a channel
        # bind the client and the server
        self.addr = addr
        # self.channel = grpc.insecure_channel(self.addr)
        # self.stub = pb2_grpc.BlackboardHandlerStub(self.channel)

    def _get_messages(self, starting_at, filter_pings=True):
        url = "http://{}/blackboard/{}".format(self.addr, starting_at)
        r = requests.get(url)
        msgs = r.json()  # iterable list of messages

        # Translate from dictionary
        msg_stack = json_format.ParseDict(msgs, pb2.MessageStack())
        return msg_stack.messages

    def _get_result_messages(self, starting_at):
        url = "http://{}/result/{}".format(self.addr, starting_at)
        r = requests.get(url)
        msgs = r.json()  # iterable list of result messages

        # Translate from dictionary
        msg_stack = json_format.ParseDict(msgs, pb2.MessageStack())
        return msg_stack.messages

    def _send_message(self, msg):
        url = "http://{}/message".format(self.addr)
        msg_json = json_format.MessageToJson(msg)
        r = requests.post(url, data=msg_json.encode("utf-8"))
