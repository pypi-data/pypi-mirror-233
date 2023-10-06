import typing
from rclpy.node import Node
from raya.handlers.cv.model_handler import ModelHandler


class RecognizerHandler(ModelHandler):

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        pass

    async def get_recognitions_once(self, as_dict=False, get_timestamp=False):
        return

    def get_current_recognitions(self, as_dict=False, get_timestamp=False):
        return

    def set_recognitions_callback(self,
                                  callback: typing.Callable = None,
                                  callback_async: typing.Callable = None,
                                  as_dict: bool = False,
                                  call_without_recognitions: bool = False):
        return

    def set_img_recognitions_callback(
            self,
            callback: typing.Callable = None,
            callback_async: typing.Callable = None,
            as_dict: bool = False,
            call_without_recognitions: bool = False,
            cameras_controller: typing.Callable = None):
        return
