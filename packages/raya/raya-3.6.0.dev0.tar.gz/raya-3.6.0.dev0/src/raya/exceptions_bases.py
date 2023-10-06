class RayaException(Exception):

    def get_raya_file(self):
        return


class RayaCodedException(RayaException):

    def __init__(self, error_code, error_msg):
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return
