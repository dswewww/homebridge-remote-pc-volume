import json

from flask import Flask, request, jsonify
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CoInitialize, CoUninitialize

from keyboard import Keyboard

api = Flask(__name__)


@api.route('/mute', methods=['POST'])
def set_mute():
    if request.get_data().decode('UTF-8') == "true":
        set_status(True, None)
    else:
        set_status(False, None)
    return get_status()


@api.route('/volume', methods=['Post'])
def set_volume():
    volume_level = int(request.get_data().decode('UTF-8'))
    if volume_level > 100 or volume_level < 0:
        return "Illegal volumeLevel", 400
    set_status(None, volume_level)
    return get_status()


@api.route('/status', methods=['GET'])
def get_status():
    CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    responseJson = {
        "Muted": [ "1" if volume.GetMute()==0else "0"],
        "VolumeLevel": [round(volume.GetMasterVolumeLevelScalar() * 100)]
    }
    CoUninitialize()
    return responseJson


def set_status(mute=None, volume_level=None):
    status = get_status()
    print(mute)
    print(status["Muted"][0])
    if (mute is True and status["Muted"][0] == "0") or (mute is False and status["Muted"][0]  == "1" ):
        Keyboard.key(Keyboard.VK_VOLUME_MUTE)
    if volume_level is not None:
        CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(round(volume_level / 100, 2), None)
        CoUninitialize()


if __name__ == '__main__':
    api.run(host='0.0.0.0')
