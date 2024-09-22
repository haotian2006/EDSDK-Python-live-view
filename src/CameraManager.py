import os
import time
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

fps = 60

edsdk.InitializeSDK()

buffer = edsdk.CreateFileStream("VideoBuffer.raw", FileCreateDisposition.OpenExisting, Access.ReadWrite)

statusPath = os.path.join(os.getcwd(),"src", "status.txt")

def detectCamera():
   while True:
       cameras = edsdk.GetCameraList()
       nr_cameras = edsdk.GetChildCount(cameras)
       if nr_cameras > 0:
           return edsdk.GetChildAtIndex(cameras, 0)
       time.sleep(1)

lines = ["0"]
def writeData():
    with open(statusPath, "w") as statusFile:
        statusFile.write("\n".join(lines))
        statusFile.flush()
       

def main():
    global evf_image,camera
    lines[0] = "0"
    writeData()
    print("Detecting camera")
    camera = detectCamera()
    lines[0] = "1"
    writeData()
    print("Opening session")
    edsdk.OpenSession(camera)

    edsdk.SetPropertyData(camera, PropID.SaveTo, 0, SaveTo.Host)
    edsdk.SetPropertyData(camera, PropID.Evf_OutputDevice, 0, EvfOutputDevice.PC)

    edsdk.SetCapacity(
        camera, {"reset": True, "bytesPerSector": 1024, "numberOfFreeClusters": 2147483647}
    )
    edsdk.SendCommand(camera, CameraCommand.DoEvfAf, EvFAf.On)
    edsdk.SendCommand(camera, CameraCommand.DriveLensEvf, 0x00000001)
    edsdk.SendCommand(camera, CameraCommand.DoEvfAf, EvFAf.On)
  
    evf_image = edsdk.CreateEvfImageRef(buffer)
    flag = True
    while flag:
        try:
            edsdk.DownloadEvfImage(camera, evf_image)
        except Exception as e:
                if str(e) != "EDS_ERR_OBJECT_NOTREADY. Image data set not ready for live view":
                        print(f"An error occurred: {e}")
                        flag = False
                       
        time.sleep(1/fps)
    try:
        edsdk.CloseSession(camera)
    except Exception as e:
        pass
    print("Session closed - Reconnecting")
    main()
main()

