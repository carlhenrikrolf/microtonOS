import subprocess

def volume(kind='volume', change=None, absolute=None):
    prefix = ['wpctl', 'set-volume', '-l', '1']
    arg1 = '@DEFAULT_AUDIO_SOURCE@' if kind == 'mic' else '@DEFAULT_AUDIO_SINK@'
    vol = subprocess.check_output(['wpctl', 'get-volume', arg1])
    vol = float(vol.decode()[8:-1])
    if change is not None:
        arg2 = str(change) + '+' if change >=0 else str(-change) + '-'
        subprocess.run([*prefix, arg1, arg2])
        return None
    elif absolute is not None:
        change = absolute/vol - 1
        volume(kind=kind, change=change)
    else:
        return vol