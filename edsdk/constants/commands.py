from enum import IntEnum


class CameraCommand(IntEnum):
    """
    CameraCommand is an enumeration of various camera commands that can be issued to control camera operations.
    Attributes:
        TakePicture (int): Command to take a picture.
        ExtendShutDownTimer (int): Command to extend the shutdown timer.
        BulbStart (int): Command to start bulb exposure.
        BulbEnd (int): Command to end bulb exposure.
        DoEvfAf (int): Command to perform autofocus in electronic viewfinder mode.
        DriveLensEvf (int): Command to drive the lens in electronic viewfinder mode.
        DoClickWBEvf (int): Command to perform white balance click in electronic viewfinder mode.
        MovieSelectSwON (int): Command to switch to movie mode.
        MovieSelectSwOFF (int): Command to switch to still image mode.
        PressShutterButton (int): Command to press the shutter button.
        RequestRollPitchLevel (int): Command to request roll and pitch level.
        DrivePowerZoom (int): Command to drive the power zoom.
        SetRemoteShootingMode (int): Command to set remote shooting mode.
        RequestSensorCleaning (int): Command to request sensor cleaning.
    """
    TakePicture = 0x00000000
    ExtendShutDownTimer = 0x00000001
    BulbStart = 0x00000002
    BulbEnd = 0x00000003
    DoEvfAf = 0x00000102
    DriveLensEvf = 0x00000103
    DoClickWBEvf = 0x00000104
    MovieSelectSwON = 0x00000107  # Change to Movie Mode
    MovieSelectSwOFF = 0x00000108  # Change to Still Image Mode
 
    PressShutterButton = 0x00000004
    RequestRollPitchLevel = 0x00000109
    DrivePowerZoom = 0x0000010d
    SetRemoteShootingMode = 0x0000010f
    RequestSensorCleaning = 0x00000112


# CameraCommand.DoEvfAf
class EvFAf(IntEnum):
    Off = 0
    On = 1


# CameraCommand.DriveLensEvf
class DriveLens(IntEnum):
    Near1 = 0x00000001
    Near2 = 0x00000002
    Near3 = 0x00000003
    Far1 = 0x00008001
    Far2 = 0x00008002
    Far3 = 0x00008003


# CameraCommand.PressShutterButton
class ShutterButton(IntEnum):
    OFF = 0x00000000
    Halfway = 0x00000001
    Completely = 0x00000003
    Halfway_NonAF = 0x00010001
    Completely_NonAF = 0x00010003


# CameraCommand.SetRemoteShootingMode
class DcRemoteShootingMode(IntEnum):
    Stop = 0
    Start = 1


# CameraCommand.DrivePowerZoom
class DrivePowerZoom(IntEnum):
    Stop = 0x00000000
    LimitOff_Wide = 0x00000001
    LimitOff_Tele = 0x00000002
    LimitOn_Wide = 0x00000011
    LimitOn_Tele = 0x00000012


# CameraCommand.RequestSensorCleaning
class RequestSensorCleaning(IntEnum):
    CleanNextTurnOn_Off = 0x00
    CleanNow = 0x01  # Note:Camera will shut down after execution.


# CameraCommand.SetModeDialDisable
class SetModeDialDisable(IntEnum):
    Cancel = 0x00
    ModeDialDisable = 0x01


# CameraCommand.RequestRollPitchLevel
class RequestRollPitchLevel(IntEnum):
    Start = 0
    Stop = 1
