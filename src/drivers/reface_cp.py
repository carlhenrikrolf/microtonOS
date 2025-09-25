# external modules
import mido
from time import sleep

# internal modules
from midi_implementation.yamaha import reface_cp as cp
from midi_implementation.midi1 import control_change as cc
from utils import Inport, Outport, make_threads, load_config

# parameters
device_name = "Reface CP"
client_name = "Reface CP Driver"
pause = 0.001

# configuration
config = {
    "general_settings": load_config(__file__, "../../config/general_settings.toml"),
    "control_change": load_config(__file__, "../../config/control_change.toml"),
}
external_channel = config["general_settings"][device_name]["channel"]
for i in range(16):
    if device_name == config["control_change"]["channel"][i]["device"]:
        internal_channel = i
received = config["control_change"]["channel"][internal_channel]["received"]


class Script:
    def __init__(self):
        self.is_local = False

    def reface_cp(self, msg):
        if not self.is_local and msg.type in ["control_change", "sysex"]:
            to_reface_cp.send(msg)
        if msg.type == "note_on" and msg.velocity == 0:
            to_microtonOS.send(
                mido.Message(
                    "note_off", note=msg.note, velocity=64, channel=internal_channel
                )
            )
        elif msg.type != "control_change":
            if hasattr(msg, "channel"):
                msg.channel = internal_channel
            to_microtonOS.send(msg)
        else:
            drive = cp.drive(msg)
            if drive is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.detune,
                        value=drive,
                        channel=internal_channel,
                    )
                )

            tremolo, depth, rate = cp.tremolo(msg)
            if tremolo is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.tremolo,
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[0],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[1],
                        value=rate,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.tremolo,
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif tremolo is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.tremolo,
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[0],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif rate is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[1],
                        value=rate,
                        channel=internal_channel,
                    )
                )

            wah, depth, rate = cp.wah(msg)
            if wah is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.sound_variation,
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[2],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[3],
                        value=rate,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.sound_variation,
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif wah is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.sound_variation,
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[2],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif rate is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[3],
                        value=rate,
                        channel=internal_channel,
                    )
                )

            chorus, depth, speed = cp.chorus(msg)
            if chorus is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.chorus,
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[4],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[5],
                        value=speed,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.chorus,
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif chorus is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.chorus,
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[4],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif speed is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[5],
                        value=speed,
                        channel=internal_channel,
                    )
                )

            phaser, depth, speed = cp.phaser(msg)
            if phaser is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.phaser,
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[6],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[7],
                        value=speed,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.phaser,
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif phaser is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.phaser,
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[6],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif speed is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[7],
                        value=speed,
                        channel=internal_channel,
                    )
                )

            digital_delay, depth, time = cp.digital_delay(msg)
            if digital_delay is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[0][0],
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[8],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[9],
                        value=time,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[0][0],
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif digital_delay is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[0][0],
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[8],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif time is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[9],
                        value=time,
                        channel=internal_channel,
                    )
                )

            analog_delay, depth, time = cp.analog_delay(msg)
            if analog_delay is True:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[1][0],
                        value=127,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[10],
                        value=depth,
                        channel=internal_channel,
                    )
                )
                sleep(pause)
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[11],
                        value=time,
                        channel=internal_channel,
                    )
                )
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[1][0],
                        value=127,
                        channel=internal_channel,
                    )
                )
            elif analog_delay is False:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.effect_controller[1][0],
                        value=0,
                        channel=internal_channel,
                    )
                )
            elif depth is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[10],
                        value=depth,
                        channel=internal_channel,
                    )
                )
            elif time is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.undefined[11],
                        value=time,
                        channel=internal_channel,
                    )
                )

            reverb = cp.reverb(msg)
            if reverb is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.reverb,
                        value=reverb,
                        channel=internal_channel,
                    )
                )

            sustain = cp.sustain(msg)
            if sustain is not None:
                to_microtonOS.send(
                    mido.Message(
                        "control_change",
                        control=cc.damper_pedal,
                        value=sustain,
                        channel=internal_channel,
                    )
                )

    def microtonOS(self, msg):
        if hasattr(msg, "channel"):
            msg.channel = external_channel
        if msg.type != "control_change":
            to_reface_cp.send(msg)
        elif msg.channel != internal_channel:
            if any(x.items() <= msg.dict().items() for x in received["sustain"]):
                pass
            elif any(x.items() <= msg.dict().items() for x in received["sostenuto"]):
                msg = cp.sostenuto(value=msg.value, channel=external_channel)
            elif any(x.items() <= msg.dict().items() for x in received["soft pedal"]):
                msg = cp.soft_pedal(value=msg.value, channel=external_channel)
            elif any(x.items() <= msg.dict().items() for x in received["modwheel"]):
                msg = cp.modwheel(value=msg.value, channel=external_channel)
            elif any(x.items() <= msg.dict().items() for x in received["expression"]):
                msg = cp.expression(value=msg.value, channel=external_channel)
            elif any(x.items() <= msg.dict().items() for x in received["volume"]):
                msg = cp.volume(value=msg.value, channel=external_channel)
            elif msg.is_cc(cc.local_onoff_switch):
                self.is_local = True if msg.value >= 64 else False
                msg = cp.local_control(cp.on if msg.value >= 64 else cp.off)
            to_reface_cp.send(msg)


# run script
to_microtonOS = Outport(client_name, name="microtonOS", verbose=False)
to_reface_cp = Outport(client_name, name="Reface CP", verbose=False)
script = Script()
from_reface_cp = Inport(script.reface_cp, client_name, name="Reface CP", verbose=False)
from_microtonOS = Inport(
    script.microtonOS, client_name, name="microtonOS", verbose=False
)
make_threads([from_reface_cp.open, from_microtonOS.open])
