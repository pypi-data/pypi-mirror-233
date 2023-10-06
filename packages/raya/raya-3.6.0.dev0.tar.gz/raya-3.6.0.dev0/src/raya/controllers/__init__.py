from typing import Union

from raya.controllers.analytics_controller import AnalyticsController
from raya.controllers.arms_controller import ArmsController
from raya.controllers.cameras_controller import CamerasController
from raya.controllers.communication_controller import CommunicationController
from raya.controllers.cv_controller import CVController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.interactions_controller import InteractionsController
from raya.controllers.leds_controller import LedsController
from raya.controllers.lidar_controller import LidarController
from raya.controllers.manipulation_controller import ManipulationController
from raya.controllers.motion_controller import MotionController
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.sensors_controller import SensorsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.status_controller import StatusController
from raya.controllers.ui_controller import UIController
from raya.controllers.nlp_controller import NLPController

ALL_CONTROLLERS_UNION = Union[
    AnalyticsController,
    ArmsController,
    CamerasController,
    CommunicationController,
    CVController,
    FleetController,
    InteractionsController,
    LedsController,
    LidarController,
    ManipulationController,
    MotionController,
    NavigationController,
    SensorsController,
    SoundController,
    StatusController,
    UIController,
    NLPController,
]
