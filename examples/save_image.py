import os
import time
import uuid

import edsdk
from edsdk import (
    CameraCommand,
    ObjectEvent,
    PropID,
    FileCreateDisposition,
    Access,
    SaveTo,
    EdsObject,
    ShutterButton,
    DriveLens
)

if os.name == "nt":
    # If you're using the EDSDK on Windows,
    # you have to have a Windows message loop in your main thread,
    # otherwise callbacks won't happen.
    # (This is because the EDSDK uses the obsolete COM STA threading model
    # instead of real threads.)
    import pythoncom
from PIL import Image
import io


def save_image(object_handle: EdsObject, save_to: str) -> int:
    dir_item_info = edsdk.GetDirectoryItemInfo(object_handle)
    raw_file_path = os.path.join(save_to, str(uuid.uuid4()) + ".raw")
    out_stream = edsdk.CreateFileStream(
        raw_file_path,
        FileCreateDisposition.CreateAlways,
        Access.ReadWrite)
    edsdk.Download(object_handle, dir_item_info["size"], out_stream)
    edsdk.DownloadComplete(object_handle)

    # Convert the raw file to a PNG image
    with open(raw_file_path, 'rb') as raw_file:
        raw_data = raw_file.read()
        image = Image.open(io.BytesIO(raw_data))
        png_file_path = raw_file_path.replace(".raw", ".png")
        image.save(png_file_path, "PNG")

    # Optionally, remove the raw file after conversion
    os.remove(raw_file_path)
    return 0


def callback_property(event, property_id: PropID, parameter: int) -> int:
    print("event: ", event)
    print("Property changed:", property_id)
    print("Parameter:", parameter)
    return 0


def callback_object(event: ObjectEvent, object_handle: EdsObject) -> int:
    print("event: ", event, "object_handle:", object_handle)
    if event == ObjectEvent.DirItemRequestTransfer:
        save_image(object_handle, ".")
    return 0


if __name__ == "__main__":
    edsdk.InitializeSDK()
    cam_list = edsdk.GetCameraList()
    nr_cameras = edsdk.GetChildCount(cam_list)

    if nr_cameras == 0:
        print("No cameras connected")
        exit(1)

    cam = edsdk.GetChildAtIndex(cam_list, 0)
    edsdk.OpenSession(cam)
    edsdk.SetObjectEventHandler(cam, ObjectEvent.All, callback_object)
    edsdk.SetPropertyData(cam, PropID.SaveTo, 0, SaveTo.Host)



    # Sets HD Capacity to an arbitrary big value
    edsdk.SetCapacity(
        cam, {"reset": True, "bytesPerSector": 512, "numberOfFreeClusters": 2147483647}
    )
    # Autofocus
    # Check if the camera supports the PressShutterButton command
    edsdk.SendCommand(cam, CameraCommand.DoEvfAf,1)
    
    edsdk.SendCommand(cam, CameraCommand.DriveLensEvf,DriveLens.Far3)
    edsdk.SendCommand(cam, CameraCommand.DriveLensEvf,DriveLens.Near2)
    # edsdk.SetPropertyData(cam, PropID.AFMode, 0, 2)
    # print(edsdk.GetPropertyData(cam, PropID.FocusInfo,2))
    #edsdk.SendCommand(cam, CameraCommand.TakePicture, 2)
    edsdk.SendCommand(cam, CameraCommand.DoEvfAf,1)
    time.sleep(1)
    edsdk.SendCommand(cam, CameraCommand.DoEvfAf,1)
    time.sleep(1)
    edsdk.SendCommand(cam, CameraCommand.DoEvfAf,0)


    time.sleep(4)
    if os.name == "nt":
        pythoncom.PumpWaitingMessages()
    edsdk.TerminateSDK()
