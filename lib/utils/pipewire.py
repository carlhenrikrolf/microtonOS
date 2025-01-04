import subprocess


def get_volume(port="@DEFAULT_AUDIO_SINK@"):
    output = subprocess.check_output(["wpctl", "get-volume", port])
    output = output.decode()
    volume = float(output[8:12])
    muted = True if "MUTED" in output else False
    return volume, muted


def get_gain():
    volume, muted = get_volume(port="@DEFAULT_AUDIO_SOURCE@")
    return volume, muted


def set_volume(level=None, muted=None, port="@DEFAULT_AUDIO_SINK@"):
    if level is not None:
        subprocess.run(["wpctl", "set-volume", port, str(level)])
    if muted is not None:
        subprocess.run(["wpctl", "set-mute", port, "1" if muted else "0"])


def set_gain(level=None, muted=None):
    set_volume(level, muted, port="@DEFAULT_AUDIO_SOURCE@")
