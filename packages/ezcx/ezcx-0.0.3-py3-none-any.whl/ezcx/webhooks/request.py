from google.cloud import dialogflowcx as cx
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse


class WebhookRequest:
    
    def __init__(self, body: dict):
        self.request = cx.WebhookRequest()
        # When a webhook comes in as JSON, we use ParseDict to convert JSON to Protobuf
        ParseDict(body, self.request._pb, ignore_unknown_fields=True)

    @property
    def tag(self):
        return self.request.fulfillment_info.tag

    @property
    def text(self):
        return self.request.text

    def to_dict(self):
        return MessageToDict(self.request._pb, including_default_value_fields=True)

    # @property
    # def session_parameters(self):
    #     return MessageToDict(self.request.session_info._pb, including_default_value_fields=True).get('parameters')

