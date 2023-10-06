import pathlib
from raya.exceptions import *
from raya.logger import RaYaLogger
from raya.skills.skill import RayaSkillHandler
from typing import NoReturn
from raya.controllers import ALL_CONTROLLERS_UNION

list_type = list
type_func = type
except_no_print_bases = [pathlib.Path(__file__).parent.resolve()]
DEPRECATED_CONTROLLER_NAMES = {'grasping': 'manipulation'}


class RayaApplicationBase():

    def __init__(self, exec_settings):
        self.log = RaYaLogger(f'RayaApp.app.{self.__app_id}')

    @__only_in_args_getting('get_argument')
    def get_argument(self,
                     *name_or_flags: str,
                     type=str,
                     required: bool = False,
                     help: str = None,
                     default=None,
                     list: bool = False,
                     **kwargs):
        return

    @__only_in_args_getting('get_flag_argument')
    def get_flag_argument(self, *name_or_flags: str, help: str = None):
        return

    def create_logger(self, name):
        return

    def register_skill(self, skill_cls) -> RayaSkillHandler:
        return

    def create_task(self, name, afunc, *args, **kargs):
        pass

    def is_task_running(self, name):
        return

    def is_task_done(self, name):
        return

    def cancel_task(self, name):
        pass

    def pop_task_return(self, name):
        return

    async def wait_for_task(self, name):
        pass

    async def sleep(self, sleep_time: float):
        pass

    def create_timer(self, name: str, timeout: float):
        pass

    def is_timer_done(self, name: str) -> bool:
        return

    def is_timer_running(self, name: str) -> bool:
        return

    @__only_in_setup('enable_controller')
    async def enable_controller(self, ctlr_name: str) -> ALL_CONTROLLERS_UNION:
        return

    @__only_in_setup('get_controller')
    async def get_controller(self, ctlr_name: str) -> ALL_CONTROLLERS_UNION:
        return

    def finish_app(self) -> NoReturn:
        pass

    def abort_app(self) -> NoReturn:
        pass
