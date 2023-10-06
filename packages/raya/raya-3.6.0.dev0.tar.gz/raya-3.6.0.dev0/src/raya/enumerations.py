from enum import IntEnum, Enum


# GENERAL


class POSITION_UNIT(IntEnum):
    '''
    Enumeration to set the unit of the coordinates in a map.
    POSITION_UNIT.PIXELS : Based on the pixel of the image map.
    POSITION_UNIT.METERS : Meters
    '''
    PIXELS = 0
    METERS = 1



class ANGLE_UNIT(IntEnum):
    '''
    Enumeration to set the angles unit.
    ANGLE_UNIT.DEGREES : Degrees
    ANGLE_UNIT.RADIANS : Radians
    '''
    DEGREES = 0
    RADIANS = 1



class SHAPE_TYPE(IntEnum):
    '''
    Enumeration to define the type of shape for obstacles.
    SHAPE_TYPE.BOX : Box
    SHAPE_TYPE.SPHERE : Sphere
    SHAPE_TYPE.CYLINDER : Cylinder
    SHAPE_TYPE.CONE : Cone
    '''
    BOX = 1
    SPHERE = 2
    CYLINDER = 3
    CONE = 4



class SHAPE_DIMENSION(IntEnum):
    '''
    Enumeration to define the array position to define the shape obstacles dimensions.
    SHAPE_DIMENSION.BOX_X : Box width
    SHAPE_DIMENSION.BOX_Y : Box large
    SHAPE_DIMENSION.BOX_Z : Box height

    SHAPE_DIMENSION.SPHERE_RADIUS : Sphere radius

    SHAPE_DIMENSION.CYLINDER_HEIGHT : Cylinder height
    SHAPE_DIMENSION.CYLINDER_RADIUS : Cylinder radius

    SHAPE_DIMENSION.CONE_HEIGHT : Cone height
    SHAPE_DIMENSION.CONE_RADIUS : Cone radius
    '''
    BOX_X = 0
    BOX_Y = 1
    BOX_Z = 2

    SPHERE_RADIUS = 0

    CYLINDER_HEIGHT = 0
    CYLINDER_RADIUS = 1

    CONE_HEIGHT = 0
    CONE_RADIUS = 1



# ARMS


class ARMS_JOINT_TYPE(IntEnum):
    '''
    Enumeration to define the type of arm joint
    ARMS_JOINT_TYPE.ROTATIONAL
    ARMS_JOINT_TYPE.LINEAR
    '''
    NOT_DEFINED = 0
    LINEAR = 1
    ROTATIONAL = 2




class ARMS_MANAGE_ACTIONS(Enum):
    '''
    Enumeration to set the action to take when the user wants to manage predefined data.
    '''
    GET = 'get'
    EDIT = 'edit'
    REMOVE = 'remove'
    GET_INFORMATION = 'get_info'
    CREATE = 'create'



# UI


class UI_INPUT_TYPE(Enum):
    '''
    Enumeration to set input type
    UI_INPUT_TYPE.TEXT: user can only input a-z or A-Z
    UI_INPUT_TYPE.NUMERIC: user can only input numbers
    '''
    TEXT = 'text'
    NUMERIC = 'numeric'



class UI_THEME_TYPE(Enum):
    '''
    Enumeration to set the UI theme type
    UI_THEME_TYPE.DARK : will specify to set background to dark
    UI_THEME_TYPE.WHITE : will specify to set background to white
    '''
    DARK = 'DARK'
    WHITE = 'WHITE'



class UI_MODAL_TYPE(Enum):
    '''
    Enumeration to set the UI modal type
    UI_MODAL_TYPE.INFO : specify that this is an informative componant, No callback
    UI_MODAL_TYPE.SUCCESS : showing a messege that the opration was seccessful
    UI_MODAL_TYPE.ERROR : showing a messege that will alert of a bad precedere
    '''
    INFO = 'info'
    SUCCESS = 'success'
    ERROR = 'error'



class UI_TITLE_SIZE(Enum):
    '''
    Enumeration to set the title size.
    UI_TITLE_SIZE.SMALL : Small size
    UI_TITLE_SIZE.MEDIUM : Medium size
    UI_TITLE_SIZE.LARGE : Large size
    '''
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'



class UI_ANIMATION_TYPE(Enum):
    '''
    Enumeration to set the animation format.
    UI_ANIMATION_TYPE.LOTTIE : Lottie format
    UI_ANIMATION_TYPE.PNG : PNG format
    UI_ANIMATION_TYPE.JPEG : JPEG format
    UI_ANIMATION_TYPE.GIF : GIF format
    UI_ANIMATION_TYPE.URL : URL format
    '''

    LOTTIE = 'LOTTIE'
    PNG = 'BASE64'
    JPEG = 'BASE64' # in reality, for UI side, it is the same as PNG
    GIF = 'BASE64'
    URL = 'URL'



class UI_SPLIT_TYPE(Enum):
    '''
    Emumeration of all the ui methods options.
    '''
    DISPLAY_MODAL = 'Modal'
    DISPLAY_SCREEN = 'DisplayScreen'
    DISPLAY_INTERACTIVE_MAP = 'InteractiveMap'
    DISPLAY_ACTION_SCRENN = 'CallToAction'
    DISPLAY_INPUT_MODAL = 'InputModal'
    DISPLAY_CHOICE_SELECTOR = 'Choice'
    DISPLAY_ANIMATION = 'Animation'
    


class UI_MODAL_SIZE(Enum):
    '''
    Enumeration to set the size of the modal.
    '''
    NORMAL = 'Normal'
    BIG = 'Big'



#LEDS


class LEDS_EXECUTION_CONTROL(IntEnum):
    '''
    Enumeration to set the animation to be overriden.
    LEDS_EXECUTION_CONTROL.OVERRIDE : Overide current animation.
    LEDS_EXECUTION_CONTROL.ADD_TO_QUEUE : Insert animation to serial queue.
    LEDS_EXECUTION_CONTROL.AFTER_CURRENT : Run animation at the end of current animation.
    '''
    OVERRIDE = 0
    ADD_TO_QUEUE = 1
    AFTER_CURRENT = 2
    


# FLEET

class FLEET_FINISH_STATUS(Enum):
    '''
    Enumeration to set indicate whether the app finished successfully or not.
    FLEET_FINISH_STATUS.SUCCESS : The app finished successfully.
    FLEET_FINISH_STATUS.FAILED : The app finished with errors or did not finish as expected.
    '''
    SUCCESS = 'Done'
    FAILED = 'Failed'

    

class FLEET_UPDATE_STATUS(Enum):
    '''
    Enumeration indicate how is the progress of the application.
    FLEET_UPDATE_STATUS.INFO : General information to the user.
    FLEET_UPDATE_STATUS.WARNING : Warning message to the user.
    FLEET_UPDATE_STATUS.SUCCESS : Success message to the user.
    FLEET_UPDATE_STATUS.ERROR : Error message to the user.
    '''
    INFO = 'Info'
    WARNING = 'Warning'
    SUCCESS = 'Success'
    ERROR = 'Error'



# STATUS


class STATUS_BATTERY(Enum):
    '''
    Enumeration to indicate the status of the battery
    '''
    UNKNOWN = 0
    CHARGING = 1
    DISCHARGING = 2
    NOT_CHARGING = 3
    FULL = 4
    NO_BATTERY = 5
    LOW_BATTERY = 6
    CRITICAL_BATTERY = 7



class STATUS_BATTERY_HEALTH(Enum):
    '''
    Enumeration to indicate the health of the battery
    '''
    UNKNOWN = 0
    GOOD = 1
    OVERHEAT = 2
    DEAD = 3
    OVERVOLTAGE = 4
    UNSPEC_FAILURE = 5
    COLD = 6
    WATCHDOG_TIMER_EXPIRE = 7
    SAFETY_TIMER_EXPIRE = 8



class STATUS_BATTERY_TECHNOLOGY(Enum):
    '''
    Enumeration to indicate the technology
    '''
    UNKNOWN = 0
    NIMH = 1
    LION = 2
    LIPO = 3
    LIFE = 4
    NICD = 5
    LIMN = 6



class STATUS_SERVER(Enum):
    '''
    Enumeration to indicate the server status
    '''
    NOT_AVAILABLE = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    FAILED = 4



class STATUS_ENGINE(Enum):
    '''
    Enumeration to indicate the engine status
    '''
    NOT_AVAILABLE = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    FAILED = 4



class STATUS_SERVER_ERROR(Enum):
    '''
    Enumeration to indicate the error code
    '''    
    OK = 0
    ERROR_UNKNOWN = 255



class STATUS_ENGINE_ERROR(Enum):
    '''
    Enumeration to indicate the error code
    '''    
    OK = 0
    ERROR_UNKNOWN = 255

