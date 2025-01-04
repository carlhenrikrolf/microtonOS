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
