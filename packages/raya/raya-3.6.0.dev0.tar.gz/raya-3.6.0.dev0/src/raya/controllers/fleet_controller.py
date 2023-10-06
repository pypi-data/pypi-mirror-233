from rclpy.node import Node
from raya.exceptions import *
from raya.controllers.base_controller import BaseController
from raya.enumerations import *
from raya.constants import *


class FleetController(BaseController):

    def __init__(self, name: str, node: Node, interface: RayaInterface,
                 extra_info):
        pass

    def set_msgs_from_fleet_callback(self, callback=None, callback_async=None):
        pass

    async def request_action(self,
                             title,
                             message,
                             task_id,
                             timeout: float = 30.0):
        return

    async def finish_task(self,
                          result: FLEET_FINISH_STATUS,
                          task_id: str,
                          message: str = None):
        pass

    async def update_app_status(self,
                                task_id: int = None,
                                status: FLEET_UPDATE_STATUS = None,
                                message: str = None):
        pass

    async def get_path(self, x: float, y: float):
        return

    async def can_navigate(self, x: float, y: float):
        return

    async def open_camera_stream(self,
                                 title: str,
                                 button_ok_txt: str,
                                 subtitle: str = '',
                                 default_camera: str = '',
                                 button_cancel_txt: str = ''):
        return
