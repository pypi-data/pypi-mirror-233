from raya.exceptions_bases import RayaException
from raya.exceptions_bases import RayaCodedException

# General exceptions
class RayaAbortException(Exception): pass
class RayaNotStarted(Exception): pass
class RayaAppFinished(Exception): pass
class RayaAppAborted(Exception): pass

# Commands
class RayaCommandException(RayaException): pass
class RayaCommandTimeout(RayaCommandException): pass
class RayaCommandFrozen(RayaCommandException): pass

# Application exceptions
class RayaApplicationException(RayaException): pass
class RayaApplicationAlreadyRegistered(RayaApplicationException): pass
class RayaApplicationNotRegistered(RayaApplicationException): pass
class RayaAppsAdminException(RayaApplicationException): pass
class RayaUnknownServerError(RayaApplicationException): pass
class RayaNotAvailableServer(RayaApplicationException): pass
class RayaNotServerPermissions(RayaApplicationException): pass
class RayaCommandAlreadyRunning(RayaApplicationException): pass
class RayaCommandNotRunning(RayaApplicationException): pass
class RayaCommandNotCancelable(RayaApplicationException): pass
class RayaCommandCanceled(RayaApplicationException): pass
class RayaGoalNotAccepted(RayaApplicationException): pass
class RayaSignalNotImplemented(RayaApplicationException): pass
class RayaSimulatorError(RayaApplicationException): pass
class RayaArgumentError(RayaApplicationException): pass
class RayaRequiredArgumentError(RayaApplicationException): pass
class RayaArgumentNotExists(RayaApplicationException): pass
class RayaOutsideSetup(RayaApplicationException): pass
class RayaCustomCommandNotAvailable(RayaApplicationException):pass
class RayaCustomMissingRequiredParameter(RayaApplicationException):pass
class RayaCustomErrorParsingParameter(RayaApplicationException):pass

# Filesystem
class RayaFileSystemException(RayaApplicationException): pass
class RayaNotValidPath(RayaFileSystemException): pass
class RayaNotDataPath(RayaFileSystemException): pass
class RayaFolderDoesNotExist(RayaFileSystemException): pass
class RayaFileDoesNotExist(RayaFileSystemException): pass
class RayaDownloadError(RayaFileSystemException): pass
class RayaWrongFileExtension(RayaFileSystemException): pass

# Skills Exceptions
class RayaSkillException(RayaException): pass
class RayaSkillWrongType(RayaSkillException): pass
class RayaSkillMissingArgument(RayaSkillException): pass
class RayaSkillUnknownArgument(RayaSkillException): pass
class RayaSkillCreationError(RayaSkillException): pass
class RayaSkillRunError(RayaSkillException): pass
class RayaSkillAlreadyInitialized(RayaSkillException): pass
class RayaSkillNotInitialized(RayaSkillException): pass
class RayaSkillAborted(RayaCodedException, RayaSkillException): pass
    
# Task Exceptions
class RayaTaskException(RayaException): pass
class RayaTaskAlreadyRunning(RayaTaskException): pass
class RayaTaskNotRunning(RayaTaskException): pass
class RayaTaskWrongFunction(RayaTaskException): pass
class RayaTaskNotAvailableReturn(RayaTaskException): pass

# Value Exceptions
class RayaValueException(RayaException): pass
class RayaInvalidNumericRange(RayaValueException): pass
class RayaInvalidRGBRange(RayaValueException): pass
class RayaInvalidHSVRange(RayaValueException): pass
class RayaWrongArgument(RayaValueException): pass

# Interface exceptions
class RayaInterfaceExceptions(RayaException): pass
class RayaNotAvailableInterface(RayaInterfaceExceptions): pass
class RayaUnknownInterface(RayaInterfaceExceptions): pass

# Controller exceptions
class RayaControllerException(RayaException): pass
class RayaNotRecognizedController(RayaControllerException): pass
class RayaAlreadyEnabledController(RayaControllerException): pass
class RayaNeedCallback(RayaControllerException): pass

# Listener Exceptions
class RayaListenerException(RayaException): pass
class RayaListenerAlreadyCreated(RayaListenerException): pass
class RayaListenerUnknown(RayaListenerException): pass
class RayaInvalidCallback(RayaListenerException): pass
class RayaWrongArgumentsNumber(RayaListenerException): pass

# Sensors Exceptions
class RayaSensorsException(RayaControllerException): pass
class RayaSensorsUnknownPath(RayaSensorsException): pass
class RayaSensorsIncompatiblePath(RayaSensorsException): pass
class RayaSensorsInvalidPath(RayaSensorsException): pass

# Lidar Exceptions
class RayaLidarInvalidAngleUnit(RayaApplicationException): pass
class RayaLidarNotDataReceived(RayaApplicationException): pass

# Cameras Exceptions
class RayaCamerasException(RayaControllerException): pass
class RayaCameraInvalidName(RayaCamerasException): pass
class RayaCameraAlreadyEnabled(RayaCamerasException): pass
class RayaCameraNotEnabled(RayaCamerasException): pass
class RayaCameraWrongType(RayaCamerasException): pass
class RayaCameraNotFrameReceived(RayaCamerasException): pass

# CV Exceptions
class RayaCVException(RayaControllerException): pass
class RayaCVUnkownError(RayaCVException): pass
class RayaCVInvalidType(RayaCVException): pass
class RayaCVInvalidModel(RayaCVException): pass
class RayaCVNotEnabledType(RayaCVException): pass
class RayaCVModelNotEnabled(RayaCVException): pass
class RayaCVModelNotDisabled(RayaCVException): pass
class RayaCVNotActiveModel(RayaCVException): pass
class RayaCVNotValidLabel(RayaCVException): pass
class RayaCVWrongModelName(RayaCVException): pass
class RayaCVNeedCallback(RayaCVException): pass
class RayaCVNeedController(RayaCVException): pass
class RayaCVAlreadyEnabled(RayaCVException): pass
class RayaCVNotCameraInterface(RayaCVException): pass
class RayaCVNotCameraEnabled(RayaCVException): pass
class RayaCVTopicNotPublishig(RayaCVException): pass
class RayaCVGPUNotAvailable(RayaCVException): pass
class RayaCVModelNotRunning(RayaCVException): pass
class RayaCVModelLimitReached(RayaCVException): pass
class RayaCVNotTrain(RayaCVException): pass
class RayaCVWrongAppInfo(RayaCVException): pass
class RayaCVWrongModelMode(RayaCVException): pass
class RayaCVNotModelMode(RayaCVException): pass
class RayaCVCameraStatusFail(RayaCVException): pass
class RayaCVWrongCamera(RayaCVException): pass
class RayaCVWrongCameraDepth(RayaCVException): pass
class RayaCVRunningOtherCamera(RayaCVException): pass
class RayaCVRunningOtherTagSize(RayaCVException): pass
class RayaCVModelNotPublishing(RayaCVException): pass
class RayaCVDiffImageNamesSize(RayaCVException): pass
class RayaCVInvalidImageFormat(RayaCVException): pass
class RayaCVInvalidModelReturn(RayaCVException): pass

## Manipulation Exceptions
class RayaManipulationException(RayaControllerException): pass
class RayaManipulationNotManipulation(RayaManipulationException): pass
class RayaManipulationAlreadyEnabled(RayaManipulationException): pass
class RayaManipulationNotArmName(RayaManipulationException): pass
class RayaManipulationObjNotFound(RayaManipulationException): pass
class RayaManipulationNotDetections(RayaManipulationException): pass
class RayaManipulationProcessFail(RayaManipulationException): pass
class RayaManipulationTopicNotPublishing(RayaManipulationException): pass
class RayaManipulationSrvNotAvailable(RayaManipulationException): pass
class RayaManipulationPickSolutionNotFound(RayaManipulationException): pass
class RayaManipulationNotReference(RayaManipulationException): pass
class RayaManipulationNotArm(RayaManipulationException): pass
class RayaManipulationNotHeight(RayaManipulationException): pass
class RayaManipulationNotTag(RayaManipulationException): pass
class RayaManipulationPlaceSolutionNotFound(RayaManipulationException): pass
class RayaManipulationInvalidPoint(RayaManipulationException): pass
class RayaManipulationNotPlaceObject(RayaManipulationException): pass

# NLP Exceptions
class RayaNlpException(RayaControllerException): pass
class RayaNlpWrongExtensionFile(RayaNlpException): pass

# Motion Exceptions
class RayaMotionException(RayaControllerException): pass
class RayaAlreadyMoving(RayaMotionException): pass
class RayaNotMoving(RayaMotionException): pass
class RayaNotValidMotionCommand(RayaMotionException): pass
class RayaObstacleDetected(RayaMotionException): pass
class RayaInvalidMinDistance(RayaMotionException): pass
class RayaMotionTimeout(RayaMotionException): pass
class RayaMotionObstacleDetected(RayaMotionException): pass
class RayaMotionUnableToMove(RayaMotionException): pass
class RayaRobotNotMoving(RayaMotionException): pass
class RayaUnableToEnableCamera(RayaMotionException): pass
class RayaNoWaitableCommand(RayaMotionException): pass


#Interactions Exceptions
class RayaInteractionsException(RayaControllerException): pass
class RayaInteractionsAlreadyRunning(RayaInteractionsException): pass
class RayaInteractionsWrongName(RayaInteractionsException): pass
class RayaInteractionsNotRunning(RayaInteractionsException): pass

# Sound Exceptions
class RayaSoundException(RayaInteractionsException): pass
class RayaSoundWrongName(RayaSoundException): pass
class RayaSoundWrongFormat(RayaSoundException): pass
class RayaSoundWrongPath(RayaSoundException): pass
class RayaSoundErrorPlatingAudiofile(RayaSoundException): pass
class RayaSoundErrorRecording(RayaSoundException): pass
class RayaSoundErrorPlayingAudio(RayaSoundException): pass
class RayaSoundBufferNotFound(RayaSoundException): pass

#LEDs Exceptions
class RayaLedsException(RayaInteractionsException): pass
class RayaLedsWrongGroup(RayaLedsException): pass
class RayaLedsWrongColor(RayaLedsException): pass
class RayaLedsWrongSpeed(RayaLedsException): pass
class RayaLedsWrongAnimationName(RayaLedsException): pass
class RayaLedsWrongRepetitions(RayaLedsException): pass

# Navigation Exceptions
class RayaNavException(RayaControllerException): pass
class RayaNavUnknownMapName(RayaNavException): pass
class RayaNavReservedMapName(RayaNavException): pass
class RayaNavAlreadyNavigating(RayaNavException): pass
class RayaNavNotNavigating(RayaNavException): pass
class RayaNavCurrentlyMapping(RayaNavException): pass
class RayaNavCantStartMapping(RayaNavException): pass
class RayaNavMapAlreadyExist(RayaNavException): pass
class RayaNavMapNameRequired(RayaNavException): pass
class RayaNavNoMapLoaded(RayaNavException): pass
class RayaNavMissingArgument(RayaNavException): pass
class RayaNavNotPathFound(RayaNavException): pass
class RayaNavNotPathBlocked(RayaNavException): pass
class RayaNavCantLocalize(RayaNavException): pass
class RayaNavPositionOutsideMap(RayaNavException): pass
class RayaNavAlreadyMapping(RayaNavException): pass
class RayaNavNotMapping(RayaNavException): pass
class RayaNavNotLocated(RayaNavException): pass
class RayaNavSortedPointsEmpty(RayaNavException): pass
class RayaNavNotPositionReceived(RayaNavException): pass
class RayaNavZoneNotFound(RayaNavException): pass
class RayaNavZonesNotFound(RayaNavException): pass
class RayaNavZoneAlreadyExist(RayaNavException): pass
class RayaNavErrorSavingZone(RayaNavException): pass
class RayaNavZoneIsNotPolygon(RayaNavException): pass
class RayaNavInvalidGoal(RayaNavException): pass
class RayaNavUnkownError(RayaNavException): pass
class RayaNavNotValidPointFound(RayaNavException): pass
class RayaNavErrorReadingYaml(RayaNavException): pass
class RayaNavErrorWritingYaml(RayaNavException): pass
class RayaNavLocationNotFound(RayaNavException): pass
class RayaNavLocationsNotFound(RayaNavException): pass
class RayaNavLocationAlreadyExist(RayaNavException): pass
class RayaNavNoDataFromMapTopic(RayaNavException): pass
class RayaNavUnableToSaveMap(RayaNavException): pass
class RayaNavUnableToChangeMap(RayaNavException): pass
class RayaUnableToFollowPath(RayaNavException): pass
class RayaUnableToComputePath(RayaNavException): pass
class RayaNoPathToGoal(RayaNavException): pass
class RayaNavIncompletePath(RayaNavException): pass
class RayaNavIncorrectPath(RayaNavException): pass
class RayaNavBadImageSize(RayaNavException): pass
class RayaNavMappingDisabled(RayaNavException): pass
class RayaNavUnableToEnableCamera(RayaNavException): pass
class RayaNavFileNotFound(RayaNavException): pass
class RayaNavWrongFileFormat(RayaNavException): pass
    
# Communication Exceptions
class RayaCommException(RayaControllerException): pass
class RayaCommTimeout(RayaControllerException): pass
class RayaCommSimultaneousRequests(RayaControllerException): pass
class RayaCommNotRunningApp(RayaCommException): pass
class RayaCommRestrictedMethod(RayaCommException): pass
class RayaCommExistingSubscription(RayaCommException): pass
class RayaCommNotExistingSubscription(RayaCommException): pass

# Skills Exceptions
class RayaSkillsException(RayaControllerException): pass
class RayaSkillsInvalidName(RayaSkillsException): pass
class RayaSkillsInvalidParameterName(RayaSkillsException): pass
class RayaSkillsMissingMandatoryParameter(RayaSkillsException): pass

# ARMS Exceptions
class RayaArmsException(RayaControllerException): pass
class RayaArmsExternalException(RayaArmsException):pass
class RayaArmsNumberOfElementsNotMatch(RayaArmsException): pass
class RayaArmsInvalidArmName(RayaArmsException):pass
class RayaArmsInvalidGroupName(RayaArmsException):pass
class RayaArmsInvalidArmOrGroupName(RayaArmsException):pass
class RayaArmsInvalidJointName(RayaArmsException):pass
class RayaArmsNotPoseArmDataAvailable(RayaArmsException):pass
class RayaArmsNotPredefinedPoseAvailable(RayaArmsException):pass
class RayaArmsInvalidNumberOfJoints(RayaArmsException):pass
class RayaArmsOutOfLimits(RayaArmsException):pass
class RayaArmsPredefinedPoseEmptyName(RayaArmsException):pass
class RayaArmsPredefinedPoseNameAlreadyExist(RayaArmsException):pass
class RayaArmsPredefinedPoseNameNotExist(RayaArmsException):pass
class RayaArmsPredefinedTrajectoryNameNotExist(RayaArmsException):pass
class RayaArmsPredefinedTrajectoryNameAlreadyExist(RayaArmsException):pass
class RayaArmsErrorParsingPredefinedTrajectory(RayaArmsException):pass
class RayaArmsInvalidCustomCommand(RayaArmsException):pass

#UI Exceptions
class RayaUIException(RayaException): pass
class RayaUIMissingValue(RayaUIException): pass
class RayaControllerNotFound(RayaUIException): pass
class RayaUIInvalidValue(RayaUIException): pass

# Fleet Exceptions
class RayaFleetException(RayaException): pass
class RayaFleetMissingValue(RayaFleetException): pass
class RayaFleetWrongResponse(RayaFleetException): pass
class RayaFleetWrongValue(RayaFleetException): pass
class RayaFleetTimeout(RayaFleetException): pass

# Status Exceptions
class RayaStatusException(RayaException): pass
class RayaStatusServerProviderDown(RayaStatusException): pass