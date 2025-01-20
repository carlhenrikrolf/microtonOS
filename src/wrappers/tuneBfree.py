import subprocess
import mido
import mtsespy as mts
from time import sleep, perf_counter_ns
from midi_implementation.midi1 import control_change as cc
from utils import Inport, Outport, handle_terminations, warmup

client_name = "tuneBfree Wrapper"
pause = 0.001
config_path = "/home/pi/microtonOS/config/"
audio_output="SonoBus"


def commandline(config):
    return [
        "/usr/bin/pw-jack",
        "/home/pi/microtonOS/third_party/tuneBfree/build/tuneBfree",
        "--noconfig",
        "--config",
        config_path + config,
        "--noprogram",
        "--program",
        config_path + "tuneBfree.pgm",
        "jack.connect=" + audio_output,
    ]


configs = ["tuneBfree.cfg", "tuneSQUAREfree.cfg", "tuneSAWfree.cfg"]
done = "All systems go. press CTRL-C, or send SIGINT or SIGHUP to terminate"
backup_cc = range(1, 120)


class Leslie:
    def __init__(self, control):
        self.control = control
        self.horn_val = 0
        self.drum_val = 0

    def translate(self, horn_value=None, drum_value=None, boost=None):
        if horn_value is not None:
            self.horn_val = horn_value
        if drum_value is not None:
            self.drum_val = drum_value
        if boost is not None:
            horn_val = self.horn_val + round(boost * (127.0 - self.horn_val) / 127.0)
            drum_val = self.drum_val + round(boost * (127.0 - self.drum_val) / 127.0)
        else:
            horn_val = self.horn_val
            drum_val = self.drum_val
        if horn_val in range(0, 42):  # horn off
            if drum_val in range(0, 42):  # drum off
                return mido.Message("control_change", control=self.control, value=8)
            elif drum_val in range(42, 84):  # drum slow
                return mido.Message("control_change", control=self.control, value=22)
            else:  # drum fast
                return mido.Message("control_change", control=self.control, value=36)
        elif horn_val in range(42, 84):  # horn slow
            if drum_val in range(0, 42):  # drum off
                return mido.Message("control_change", control=self.control, value=50)
            elif drum_val in range(42, 84):  # drum slow
                return mido.Message("control_change", control=self.control, value=64)
            else:  # drum fast
                return mido.Message("control_change", control=self.control, value=78)
        else:  # horn fast
            if drum_val in range(0, 42):  # drum off
                return mido.Message("control_change", control=self.control, value=92)
            elif drum_val in range(42, 84):  # drum slow
                return mido.Message("control_change", control=self.control, value=106)
            else:  # drum fast
                return mido.Message("control_change", control=self.control, value=120)


class Vibrato:
    def __init__(self, control):
        self.control = control
        self.depth_val = 0
        self.is_chorus_val = 0

    def translate(self, depth=None, is_chorus=None):
        if depth is not None:
            self.depth_val = depth
        if is_chorus is not None:
            self.is_chorus_val = is_chorus
        if self.depth_val in range(0, 42):  # 1
            if self.is_chorus_val in range(0, 64):  # v
                return mido.Message("control_change", control=self.control, value=11)
            else:  # c
                return mido.Message("control_change", control=self.control, value=32)
        elif self.depth_val in range(42, 84):  # 2
            if self.is_chorus_val in range(0, 64):  # v
                return mido.Message("control_change", control=self.control, value=53)
            else:  # c
                return mido.Message("control_change", control=self.control, value=74)
        else:  # 3
            if self.is_chorus_val in range(0, 64):  # v
                return mido.Message("control_change", control=self.control, value=95)
            else:  # c
                return mido.Message("control_change", control=self.control, value=116)


leslie = Leslie(control=1)
vibrato = Vibrato(control=13)


def drive(msg):
    if msg.is_cc(cc.detune):
        if msg.value > 0:
            to_tuneBfree.send(mido.Message("control_change", control=8, value=127))
        else:
            to_tuneBfree.send(mido.Message("control_change", control=8, value=0))
        sleep(pause)
        to_tuneBfree.send(mido.Message("control_change", control=9, value=msg.value))


def horn(msg):
    if msg.is_cc(cc.tremolo):
        if msg.value in range(0, 64):
            to_tuneBfree.send(leslie.translate(horn_value=0))
    elif msg.is_cc(cc.undefined[0]):
        to_tuneBfree.send(mido.Message("control_change", control=2, value=msg.value))
        sleep(pause)
        to_tuneBfree.send(mido.Message("control_change", control=3, value=msg.value))
    elif msg.is_cc(cc.undefined[1]):
        to_tuneBfree.send(leslie.translate(horn_value=msg.value))


def wah(msg):
    if msg.is_cc(cc.undefined[2]):
        to_tuneBfree.send(mido.Message("control_change", control=4, value=msg.value))
    elif msg.is_cc(cc.undefined[3]):
        to_tuneBfree.send(mido.Message("control_change", control=5, value=msg.value))


def chorus(msg):
    if msg.is_cc(cc.chorus):
        if msg.value in range(0, 64):
            to_tuneBfree.send(
                mido.Message("control_change", control=12, value=0)
            )  # vibrato off
        else:
            to_tuneBfree.send(
                mido.Message("control_change", control=12, value=96)
            )  # vibrato on
    elif msg.is_cc(cc.undefined[4]):
        to_tuneBfree.send(vibrato.translate(depth=msg.value))
    elif msg.is_cc(cc.undefined[5]):
        to_tuneBfree.send(vibrato.translate(is_chorus=msg.value))


def drum(msg):
    if msg.is_cc(cc.phaser):
        if msg.value in range(0, 64):
            to_tuneBfree.send(leslie.translate(drum_value=0))
    elif msg.is_cc(cc.undefined[6]):
        to_tuneBfree.send(mido.Message("control_change", control=6, value=msg.value))
        sleep(pause)
        to_tuneBfree.send(mido.Message("control_change", control=7, value=msg.value))
    elif msg.is_cc(cc.undefined[7]):
        to_tuneBfree.send(leslie.translate(drum_value=msg.value))


def harmonic2(msg):
    if msg.is_cc(cc.effect_controller[0][0]):
        to_tuneBfree.send(mido.Message("control_change", control=14, value=msg.value))
        sleep(pause)
        to_tuneBfree.send(mido.Message("control_change", control=15, value=127))
    elif msg.is_cc(cc.undefined[8]):
        to_tuneBfree.send(mido.Message("control_change", control=16, value=msg.value))
    elif msg.is_cc(cc.undefined[9]):
        to_tuneBfree.send(mido.Message("control_change", control=17, value=msg.value))


def harmonic3(msg):
    if msg.is_cc(cc.effect_controller[1][0]):
        to_tuneBfree.send(mido.Message("control_change", control=14, value=msg.value))
        sleep(pause)
        to_tuneBfree.send(mido.Message("control_change", control=15, value=0))
    elif msg.is_cc(cc.undefined[10]):
        to_tuneBfree.send(mido.Message("control_change", control=16, value=msg.value))
    elif msg.is_cc(cc.undefined[11]):
        to_tuneBfree.send(mido.Message("control_change", control=17, value=msg.value))


def reverb(msg):
    if msg.is_cc(cc.reverb):
        to_tuneBfree.send(mido.Message("control_change", control=10, value=msg.value))


def expression(msg):
    if msg.is_cc(cc.expression_controller[0]):
        to_tuneBfree.send(mido.Message("control_change", control=11, value=msg.value))
    elif msg.is_cc(cc.soft_pedal):
        value = 127 - round(msg.value / 2)
        to_tuneBfree.send(mido.Message("control_change", control=11, value=value))


def dispatch(msg):
    if msg.channel in range(1, 13):
        to_tuneBfree.send(msg.copy(channel=1))
    elif msg.channel == 13:
        to_tuneBfree.send(msg.copy(channel=1))
    elif msg.channel == 14:
        to_tuneBfree.send(msg.copy(channel=0))
    else:
        to_tuneBfree.send(msg.copy(channel=0))


def all_notes_off(msg):
    if msg.is_cc(cc.all_notes_off):
        for channel in range(0, 3):
            for note in range(0, 128):
                to_tuneBfree.send(mido.Message("note_off", note=note, channel=channel))


class Script:
    def __init__(self):
        self.bank = 0
        self.program = 0
        self.process = subprocess.Popen(commandline(configs[self.bank]))
        handle_terminations(self.process)
        self.to_frequency = [0.0] * 128
        for note in range(0, 128):
            self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
        self.control_to_value = [None] * 128

    def run(self, msg):
        if msg.is_cc(cc.bank_select[0]):
            self.bank = msg.value
            self.load()
        elif msg.type == "control_change":
            if msg.control in backup_cc:
                self.control_to_value[msg.control] = msg.value
                drive(msg)
                horn(msg)
                wah(msg)
                chorus(msg)
                drum(msg)
                harmonic2(msg)
                harmonic3(msg)
                reverb(msg)
                expression(msg)
            else:
                all_notes_off(msg)
        elif msg.type in ["aftertouch", "polytouch"]:
            to_tuneBfree.send(leslie.translate(boost=msg.value))
        elif msg.type == "program_change":
            self.program = msg.program
            self.resend()
        elif hasattr(msg, "channel"):
            dispatch(msg)
            self.restart(msg)
        else:
            to_tuneBfree.send(msg)

    def restart(self, msg):
        if msg.type == "note_on":
            new_frequency = mts.note_to_frequency(mts_client, msg.note, 0)
            if new_frequency != self.to_frequency[msg.note]:
                for note in range(0, 128):
                    self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
                self.load()
                self.resend()
                self.run(msg)

    def load(self):
        try:
            self.process.terminate()
        finally:
            self.process = subprocess.Popen(
                commandline(configs[self.bank]),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            start = perf_counter_ns()
            for line in iter(self.process.stdout.readline, b""):
                if done in line.decode():
                    print(
                        "tuneBfree took",
                        (perf_counter_ns() - start) / 1e9,
                        "seconds to load",
                    )
                    break
                elif perf_counter_ns() - start > 5e9:
                    print("tuneBfree has not loaded after 5 seconds, moving on ...")
                    break
            self.process.stdout = None
            self.process.stderr = None

    def resend(self):
        to_tuneBfree.send(mido.Message("program_change", program=self.program))
        sleep(pause)
        for control, value in enumerate(self.control_to_value):
            if control in backup_cc and value is not None:
                self.run(mido.Message("control_change", control=control, value=value))
                sleep(pause)


warmup.client()
with mts.Client() as mts_client:
    to_tuneBfree = Outport(client_name, verbose=False)
    script = Script()
    from_microtonOS = Inport(script.run, client_name, verbose=False)
    from_microtonOS.open()
