import typing
from typing import List
from rclpy.node import Node
from raya.constants import *
from raya_constants.interfaces import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya.exceptions import *

SIZE = 20
SIZE_PART_BUFFER = (640 * 1024)


class SoundData():

    def __init__(self,
                 channels=1,
                 sample_rate=8000,
                 sample_format=SAMPLE_S16LE,
                 coding_format='PCM'):
        self.channels = channels
        self.sample_rate = sample_rate
        self.sample_format = sample_format
        self.coding_format = coding_format

    @property
    def data(self):
        return

    @data.setter
    def data(self, data):
        pass

    def clearData(self):
        pass

    @property
    def channels(self):
        return

    @property
    def sample_rate(self):
        return

    @property
    def sample_format(self):
        return

    @property
    def coding_format(self):
        return

    @channels.setter
    def channels(self, value: int):
        pass

    @sample_rate.setter
    def sample_rate(self, value: int):
        pass

    @sample_format.setter
    def sample_format(self, value: int):
        pass

    @coding_format.setter
    def coding_format(self, value: str):
        pass

    def getSampleWidth(self):
        return


class SoundController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    async def play_sound_from_file(self,
                                   filepath: str,
                                   volume: int = 100,
                                   callback_feedback=None,
                                   callback_finish=None,
                                   wait=True) -> None:
        return

    async def play_sound_from_data(self,
                                   audio_raw: list,
                                   volume: int = 100,
                                   callback_feedback=None,
                                   callback_finish=None,
                                   wait=True) -> None:
        return

    async def play_predefined_sound(self,
                                    sound_name: str,
                                    volume: int = 100,
                                    callback_feedback=None,
                                    callback_finish=None,
                                    wait=True) -> None:
        return

    def get_predefined_sounds(self) -> List[str]:
        return

    async def record_sound(self,
                           duration: float = 60.0,
                           mic_id: str = '',
                           path: str = '',
                           callback_finish: typing.Callable = None,
                           callback_finish_async: typing.Callable = None,
                           wait: bool = True) -> SoundData:
        return

    def is_playing(self):
        return

    def is_recording(self):
        return

    async def play_sound(self,
                         name: str = None,
                         path: str = None,
                         data: SoundData = None,
                         volume: int = 100,
                         callback_finish: typing.Callable = None,
                         callback_finish_async: typing.Callable = None,
                         callback_feedback: typing.Callable = None,
                         callback_feedback_async: typing.Callable = None,
                         wait: bool = True) -> None:
        pass

    async def cancel_sound(self):
        pass
