from raya.skills.skill import RayaSkill


class RayaFSMException(Exception):
    pass


class RayaFSMAlreadyRegisteredFSM(RayaFSMException):
    pass


class RayaFSMMissinTransition(RayaFSMException):
    pass


class RayaFSMNotCallableMethod(RayaFSMException):
    pass


class RayaFSMNotAsyncMethod(RayaFSMException):
    pass


class RayaFSMInvalidState(RayaFSMException):
    pass


class RayaFSMInvalidInitialState(RayaFSMException):
    pass


class RayaFSMInvalidEndState(RayaFSMException):
    pass


class RayaFSMUnknownState(RayaFSMException):
    pass


class RayaFSMInvalidTransition(RayaFSMException):
    pass


class RayaFSMNotRunning(RayaFSMException):
    pass


class RayaFSMInvalidErrorCode(RayaFSMException):
    pass


class RayaFSMMissingRequiredArgument(RayaFSMException):
    pass


class RayaFSMSkill(RayaSkill):

    def set_state(self, state):
        pass

    async def main(self):
        self.main_result = None
        return
