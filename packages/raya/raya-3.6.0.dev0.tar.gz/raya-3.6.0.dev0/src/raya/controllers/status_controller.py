from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from raya.enumerations import ANGLE_UNIT, POSITION_UNIT
from raya.constants import *
from raya_constants.interfaces import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya.exceptions import *

TIME_TIMEOUT_SRV = DEFAULT_COMMAND_TIMEOUT
RAYA_SIM_ENV_NAME = 'RAYA_SIM'
TOPIC_SENSORS = 'battery_state'
TOPIC_APPS_RUNNING = 'apps_running'
TOPIC_LOCATION_STATUS = 'localization_status'
TIMEOUT_TOPIC_UNAVAILABLE = 5.0
TIMEOUT_SERVER_TASK = 0.5
MIN_TIMER_SERVER_TASK = 10
ERROR_SERVER_PROVIDER_DOWN = 'The server provider is not available'


class StatusController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        self.timer = self._node.create_timer(
            TIME_SERVER_TASK,
            self.__check_server_status,
            callback_group=ReentrantCallbackGroup())

    async def get_raya_status(self) -> dict:
        return

    async def get_battery_status(self) -> dict:
        return

    async def get_localization_status(self, ang_unit: ANGLE_UNIT,
                                      pos_unit: POSITION_UNIT) -> dict:
        return

    async def get_manipulation_status(self) -> dict:
        pass

    async def get_available_arms(self) -> dict:
        pass
