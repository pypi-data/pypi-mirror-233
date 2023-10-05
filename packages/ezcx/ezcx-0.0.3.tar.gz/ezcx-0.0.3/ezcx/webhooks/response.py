from typing import List

from google.cloud import dialogflowcx as cx

from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

# Text = cx.ResponseMessage.Text
# LiveAgentHandoff = cx.ResponseMessage.LiveAgentHandoff
# ConversationSuccess = cx.ResponseMessage.ConversationSuccess
# OutputAudioText = cx.ResponseMessage.OutputAudioText
# PlayAudio = cx.ResponseMessage.PlayAudio
# MixedAudio = cx.ResponseMessage.MixedAudio
# TelephonyTransferCall = cx.ResponseMessage.TelephonyTransferCall


class WebhookResponse:
    
    def __init__(self):
        fulfillment_response = self.FulfillmentResponse(messages=[])
        self.response: cx.WebhookResponse = cx.WebhookResponse(
            fulfillment_response=fulfillment_response
        )

    @property
    def FulfillmentResponse(self):
        return cx.WebhookResponse.FulfillmentResponse

    @property
    def ResponseMessage(self):
        return cx.ResponseMessage

    @property
    def Text(self):
        return cx.ResponseMessage.Text

    @property
    def OutputAudioText(self):
        return cx.ResponseMessage.OutputAudioText

    @property
    def LiveAgentHandoff(self):
        return cx.ResponseMessage.LiveAgentHandoff

    @property
    def TelephonyTransferCall(self):
        return cx.ResponseMessage.TelephonyTransferCall

    @property
    def fulfillment_response(self):
        return self.response.fulfillment_response

    def add_response(self, response_message: cx.ResponseMessage):
        self.fulfillment_response.messages.append(response_message)
        return self

    def add_text_response(self, *texts):
        text = self.Text(text=texts)
        response_message = self.ResponseMessage(text=text)
        self.add_response(response_message)
        return self
    
    def add_ssml_response(self, ssml: str):
        output_audio_text = self.OutputAudioText(ssml=ssml)
        response_message = cx.ResponseMessage(output_audio_text=output_audio_text)
        self.add_response(response_message)
        return self

    def add_session_parameters(self, parameters: dict):
        session_info = cx.SessionInfo(parameters=parameters)
        self.response.session_info = session_info
        return self

    def add_telephony_transfer_call(self, phone_number: str):
        telephony_transfer = self.TelephonyTransferCall(phone_number=phone_number)
        self.add_response(telephony_transfer)
        return self

    def to_dict(self):
        return MessageToDict(self.response._pb, including_default_value_fields=True)


