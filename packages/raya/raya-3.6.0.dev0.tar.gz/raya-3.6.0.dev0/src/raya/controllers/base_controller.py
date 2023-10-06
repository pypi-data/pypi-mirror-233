from rclpy.node import Node
from raya.constants import *
from raya_constants.interfaces import *
from raya.exceptions import *
from raya.constants import *
from raya.exceptions_handler import *


class CommandHandler():

    def __init__(self,
                 cb_finish,
                 cb_finish_async,
                 cb_feedback,
                 cb_feedback_async,
                 result_future,
                 result_handler,
                 last_command_loop_time=None,
                 parse_result_field_as_dict=False):
        self.cb_finish = cb_finish
        self.cb_finish_async = cb_finish_async
        self.cb_feedback = cb_feedback
        self.cb_feedback_async = cb_feedback_async
        self.result_future = result_future
        self.result_handler = result_handler
        self.last_command_loop_time = last_command_loop_time
        self.parse_result_field_as_dict = parse_result_field_as_dict


class BaseController():

    def __init__(self,
                 name: str,
                 node: Node,
                 interface: RayaInterface,
                 extra_info={}):
        pass

    async def specific_robot_command(self,
                                     name: str,
                                     parameters: dict,
                                     callback_done=None,
                                     callback_feedback=None,
                                     wait=False):
        return

    def delete_listener(self, listener_name):
        pass
