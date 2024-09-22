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
    EvfOutputDevice,
    EvFAf,
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
import tkinter as tk
from PIL import ImageTk


def save_image(object_handle: EdsObject, save_to: str) -> int:
    print("Saving image")
    dir_item_info = edsdk.GetDirectoryItemInfo(object_handle)
    raw_file_path = os.path.join(save_to, str(uuid.uuid4()) + ".raw")
    out_stream = edsdk.CreateFileStream(
        raw_file_path,
        FileCreateDisposition.CreateAlways,
        Access.ReadWrite)
    edsdk.Download(object_handle, dir_item_info["size"], out_stream)
    edsdk.DownloadComplete(object_handle)

    with open(raw_file_path, 'rb') as raw_file:
        raw_data = raw_file.read()
        image = Image.open(io.BytesIO(raw_data))
        png_file_path = raw_file_path.replace(".raw", ".png")
        image.save(png_file_path, "PNG")

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

window_width = 768  
window_height = 512

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
    edsdk.SetPropertyData(cam, PropID.Evf_OutputDevice, 0, EvfOutputDevice.PC)

    edsdk.SetCapacity(
        cam, {"reset": True, "bytesPerSector": 1024, "numberOfFreeClusters": 2147483647}
    )
 


    edsdk.SendCommand(cam, CameraCommand.DoEvfAf, EvFAf.On)
    edsdk.SendCommand(cam, CameraCommand.DriveLensEvf, 0x00000001)
    edsdk.SendCommand(cam, CameraCommand.DoEvfAf, EvFAf.On)
    image = edsdk.CreateFileStream("test.raw", FileCreateDisposition.CreateAlways, Access.ReadWrite)
    evf_image = edsdk.CreateEvfImageRef(image)
    
    zoom = 1
    
    def zoom(event=None):
        global zoom
        zoom = 1 if zoom == 5 else 5
        edsdk.SetPropertyData(cam, PropID.Evf_Zoom, 0, zoom)

    def focusUp(event=None):
        edsdk.SendCommand(cam, CameraCommand.DriveLensEvf, DriveLens.Far3)
    def focusDown(event=None):
        edsdk.SendCommand(cam, CameraCommand.DriveLensEvf, DriveLens.Near3)

    def update_frame():
        try:
            global evf_image
            edsdk.DownloadEvfImage(cam, evf_image)

            raw_file_path = os.path.join('.', "test.raw")
            with open(raw_file_path, 'rb') as raw_file:
                raw_data = raw_file.read()
                image = Image.open(io.BytesIO(raw_data))
                photo = ImageTk.PhotoImage(image)

                canvas.delete("all")
                canvas.create_image(window_width // 2, window_height // 2, image=photo, anchor=tk.CENTER)
                canvas.image = photo
        except edsdk.EdsError as e:
                if str(e) == "EDS_ERR_OBJECT_NOTREADY. Image data set not ready for live view":
                    return root.after(16, update_frame)
                print(f"An error occurred: {e}")
        root.after(16, update_frame)

    root = tk.Tk()
    root.title("Live View")
    label = tk.Label(root)
    label.pack()

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    root.bind("<Button-2>", zoom)
    root.bind("<MouseWheel>", lambda event: focusUp() if event.delta > 0 else focusDown())

    update_frame()
    root.mainloop()

    edsdk.CloseSession(cam)
    edsdk.TerminateSDK()