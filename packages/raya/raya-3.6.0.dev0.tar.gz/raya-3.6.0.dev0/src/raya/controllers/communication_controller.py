from rclpy.node import Node
from raya.exceptions import *
from raya.constants import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya_constants.interfaces import *


class MQTTSubscriptionHandler():

    def __init__(self, callback, callback_async):
        self.callback = callback
        self.callback_async = callback_async


class CommunicationController(BaseController):

    def __init__(self, name: str, node: Node, interface: RayaInterface,
                 extra_info):
        pass

    async def mqtt_publish_message(self, topic: str, data: dict):
        pass

    async def mqtt_create_subscription(self,
                                       topic: str,
                                       callback=None,
                                       callback_async=None):
        pass

    def mqtt_remove_subscription(self, topic: str):
        pass
