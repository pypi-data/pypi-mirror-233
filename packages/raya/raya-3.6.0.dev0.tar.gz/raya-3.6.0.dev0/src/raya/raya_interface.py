from raya.controllers.sensors_controller import SensorsController
from raya.controllers.lidar_controller import LidarController
from raya.controllers.motion_controller import MotionController
from raya.controllers.cameras_controller import CamerasController
from raya.controllers.interactions_controller import InteractionsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.leds_controller import LedsController
from raya.controllers.cv_controller import CVController
from raya.controllers.manipulation_controller import ManipulationController
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.communication_controller import CommunicationController
from raya.controllers.arms_controller import ArmsController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.analytics_controller import AnalyticsController
from raya.controllers.status_controller import StatusController
from raya.controllers.nlp_controller import NLPController
from raya.controllers.rgs_controller import RGSController

CONTROLLERS = {
    'sensors': (SensorsController, ['sensors']),
    'lidar': (LidarController, ['sensors']),
    'motion': (MotionController, ['motion']),
    'cameras': (CamerasController, ['cameras']),
    'interactions': (InteractionsController, ['interactions']),
    'sound': (SoundController, ['interactions']),
    'leds': (LedsController, ['interactions']),
    'cv': (CVController, ['cv']),
    'arms': (ArmsController, ['arms']),
    'manipulation': (ManipulationController, ['manipulation']),
    'navigation': (NavigationController, ['nav']),
    'status': (StatusController, []),
    'rgs': (RGSController, ['communication']),
    'communication': (CommunicationController, ['communication']),
    'arms': (ArmsController, ['arms']),
    'nlp': (NLPController, ['nlp']),
    'ui': (UIController, ['communication']),
    'fleet': (FleetController, ['communication']),
    'analytics': (AnalyticsController, ['communication'])
}
PSEUDO_CONTROLLERS = {}
PSEUDO_CONTROLLERS_DEPENDECIES = {}


class RayaInterface():

    def __init__(self, app_id: str):
        pass

    def get_app_name(self):
        return

    async def stop_all_running_commands(self):
        pass
