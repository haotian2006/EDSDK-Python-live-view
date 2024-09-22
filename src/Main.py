from PIL import Image,ImageTk
import io
import tkinter as tk
import subprocess
import threading
import time
import os

window_width = 768  
window_height = 512
fps = 59

cameraManagerPath =  os.path.join(os.getcwd(),"src", "CameraManager.py")
statusPath = os.path.join(os.getcwd(), "src","status.txt")

root = tk.Tk()
root.title("Live View")
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

crashed = False

def Render():
    try:
        data = ["0"]
        with open(statusPath, "r") as statusFile:
            lines = statusFile.readlines()
            i = 0
            for line in lines:
                data[i] = line
                i += 1  
        with open("VideoBuffer.raw", 'rb') as raw_file:
            raw_data = raw_file.read()
            image = Image.open(io.BytesIO(raw_data))
            photo = ImageTk.PhotoImage(image)
            canvas.delete("all")
            canvas.create_image(window_width // 2, window_height // 2, image=photo, anchor=tk.CENTER)
            canvas.image = photo
            if crashed:
               canvas.create_text(window_width // 2, window_height // 2, text="Crashed, Reconnecting", fill="red", font=("Arial", 16))
            if data[0] == "0":
                canvas.create_text(window_width // 2, window_height // 2, text="No camera detected", fill="red", font=("Arial", 16))

    except Exception as e:
        pass

    root.after((int)(1000/fps), Render)

Render()

# for some reason the camera manager just crashes when a camera disconnects sometimes
def run_camera_manager():
    global crashed
    while True:
        crashed = False
        process = subprocess.Popen(["python", cameraManagerPath])
        process.wait()
        crashed = True

        if process.returncode != 0:
            print(f"Script crashed with exit code {process.returncode}")
        else:
            print("Script exited normally")
        time.sleep(2)
        

camera_thread = threading.Thread(target=run_camera_manager)
camera_thread.start()

root.mainloop()