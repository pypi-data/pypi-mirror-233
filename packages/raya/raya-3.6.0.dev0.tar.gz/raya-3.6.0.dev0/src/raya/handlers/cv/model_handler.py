import typing
from rclpy.node import Node


class ModelHandler():

    def __init__(self, node: Node, topic: str, source: str, model_id: int,
                 model_info: dict, continues_msg: bool, cli_cmd, cmd_call):
        self.class_type = topic.split('/')[(-1)].split('_')[0]
        self.model_id = model_id
        self.cli_cmd = cli_cmd

    async def get_predictions_once(self, as_dict=False, get_timestamp=False):
        pass

    def get_current_predictions(self, as_dict=False, get_timestamp=False):
        pass

    def set_predictions_callback(self,
                                 callback: typing.Callable = None,
                                 callback_async: typing.Callable = None,
                                 as_dict: bool = False,
                                 call_without_predictions: bool = False):
        pass

    def set_img_predictions_callback(
            self,
            callback: typing.Callable = None,
            callback_async: typing.Callable = None,
            as_dict: bool = False,
            call_without_predictions: bool = False,
            cameras_controller: typing.Callable = None):
        pass

    def cancel_finds(self):
        pass
