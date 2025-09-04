import subprocess
import re


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


def set_volume4all(level=None, muted=None):
    status = subprocess.check_output(["wpctl", "status"])
    status = status.decode()
    # find the integer ids of all audio sinks
    sinks_section = re.search(
        r"Sinks:\n(.*?)(?=\n\s*(?:├─|└─)?\s*\w+ endpoints:|\n\s*├─ Sources:|$)",
        status,
        re.DOTALL,
    )
    ports = []
    if sinks_section:
        # Regex to find lines starting with an optional tree character, optional '*',
        # whitespace, and then capturing the numerical ID.
        ports = re.findall(
            r"^\s*(?:│|\s)?\s*(?:\*\s*)?(\d+)\.", sinks_section.group(1), re.MULTILINE
        )
    print(ports)
    for port in ports:
        set_volume(level, muted, port=port)


def set_gain4all(level=None, muted=None):
    status = subprocess.check_output(["wpctl", "status"])
    status = status.decode()
    # find the integer ids of all audio sources
    sources_section = re.search(
        r"Sources:\n(.*?)(?=\n\s*(?:├─|└─)?\s*\w+ endpoints:|$)", status, re.DOTALL
    )
    ports = []
    if sources_section:
        # Regex to find lines starting with an optional tree character, optional '*',
        # whitespace, and then capturing the numerical ID.
        ports = re.findall(
            r"^\s*(?:│|\s)?\s*(?:\*\s*)?(\d+)\.", sources_section.group(1), re.MULTILINE
        )
    print(ports)
    for port in ports:
        set_gain(level, muted, port=port)


def set_gain(level=None, muted=None, port="@DEFAULT_AUDIO_SOURCE@"):
    set_volume(level, muted, port=port)
