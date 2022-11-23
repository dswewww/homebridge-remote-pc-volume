from flask import Flask, json, app
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CoInitialize, CoUninitialize

from keyboard import Keyboard

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)


@api.route('/mute', methods=['GET'])
def set_mute():
    muted = ""
    CoInitialize()
    Keyboard.key(Keyboard.VK_VOLUME_MUTE)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    #volume.SetMasterVolumeLevel(-20.0, None)
    volume.GetVolumeRange()
    muted = volume.GetMute()
    print(muted)
    CoUninitialize()

    # volume.SetMute()
    return "Muted"if muted == 1else "Unmuted"

@api.route('/mute_state', methods=['GET'])
def get_mute():
    muted = ""
    CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volume.GetVolumeRange()
    muted = volume.GetMute()
    print(muted)
    CoUninitialize()
    # volume.SetMute()
    return "Muted"if muted == 1else "Unmuted"


if __name__ == '__main__':
    api.run(host = '0.0.0.0')
