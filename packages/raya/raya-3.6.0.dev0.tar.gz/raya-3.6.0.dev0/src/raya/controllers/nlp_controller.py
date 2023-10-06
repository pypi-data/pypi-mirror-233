import typing
from rclpy.node import Node
from raya.controllers.base_controller import BaseController


class NLPController(BaseController):

    def __init__(self, name: str, node: Node, app, extra_info={}):
        pass

    async def stt_set_provider(self,
                               provider,
                               credentials_json='',
                               credentials_file=None):
        pass

    async def tts_set_provider(self,
                               provider,
                               credentials_json='',
                               credentials_file=None):
        pass

    async def stt_transcribe_from_file(
            self,
            file,
            language,
            callback_feedback: typing.Callable = None,
            callback_feedback_async: typing.Callable = None,
            callback_finish: typing.Callable = None,
            callback_finish_async: typing.Callable = None,
            wait: bool = False):
        return

    async def stt_transcribe_from_mic(
            self,
            microphone,
            voice_detector,
            language,
            timeout,
            callback_feedback: typing.Callable = None,
            callback_feedback_async: typing.Callable = None,
            callback_finish: typing.Callable = None,
            callback_finish_async: typing.Callable = None,
            wait: bool = False):
        return

    async def tts_play_text(self,
                            text,
                            voice,
                            language,
                            callback_feedback: typing.Callable = None,
                            callback_feedback_async: typing.Callable = None,
                            callback_finish: typing.Callable = None,
                            callback_finish_async: typing.Callable = None,
                            wait: bool = False):
        return
