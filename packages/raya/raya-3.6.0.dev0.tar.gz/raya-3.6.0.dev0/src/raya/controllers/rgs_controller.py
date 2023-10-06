from rclpy.node import Node
from raya.exceptions import *
from raya.constants import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya_constants.interfaces import *
from raya_communication_msgs.msg import MsgToRGS


class RGSController(BaseController):

    def __init__(self, name: str, node: Node, interface: RayaInterface,
                 extra_info):
        pass

    def loads_from_msg(self, msg: MsgToRGS):
        return

    async def send_msg_to_app(self,
                              app_id: str,
                              controller: str,
                              header: dict = {},
                              data: dict = {}) -> None:
        pass

    def set_incoming_msg_callback(self, callback=None, callback_async=None):
        pass

    async def get_id(self):
        return
