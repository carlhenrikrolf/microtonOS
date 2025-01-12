import mido
from time import sleep
from midi_implementation.yamaha import reface_cp as cp
from midi_implementation.midi1 import control_change as cc
from utils import Inport, Outport, make_threads

client_name = "Reface CP Driver"
pause = 0.001


def get_pedal(string):
    if string == "Rd I":
        return cc.damper_pedal
    elif string == "Rd II":
        return cc.sostenuto
    elif string == "Wr":
        return cc.soft_pedal
    elif string == "Clv":
        return cc.expression_controller[0]
    elif string == "Toy":
        return cc.foot_controller[1]
    else:
        return cc.hold2


class Script:
    def __init__(self):
        self.pedal = cc.damper_pedal

    def reface_cp(self, msg):
        if msg.type == "control_change":
            to_reface_cp.send(msg)
        else:
            to_microtonOS.send(msg)

        instrument_type = cp.instrument_type(msg)
        if instrument_type is not None:
            if self.pedal == cc.expression_controller[0]:
                to_microtonOS.send(
                    mido.Message("control_change", control=self.pedal, value=127)
                )
            elif self.pedal == cc.foot_controller[1]:
                to_microtonOS.send(
                    mido.Message(
                        "control_change", control=cc.foot_controller[0], value=0
                    )
                )
            else:
                to_microtonOS.send(
                    mido.Message("control_change", control=self.pedal, value=0)
                )
            sleep(pause)
            self.pedal = get_pedal(instrument_type)
            if self.pedal == cc.expression_controller[0]:
                to_microtonOS.send(
                    mido.Message("control_change", control=self.pedal, value=0)
                )
            elif self.pedal == cc.foot_controller[1]:
                to_microtonOS.send(
                    mido.Message(
                        "control_change", control=cc.foot_controller[0], value=127
                    )
                )
            else:
                to_microtonOS.send(
                    mido.Message("control_change", control=self.pedal, value=127)
                )

        drive = cp.drive(msg)
        if drive is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.detune, value=drive)
            )

        tremolo, depth, rate = cp.tremolo(msg)
        if tremolo is True:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.tremolo, value=127)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[0], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[1], value=rate)
            )
        elif tremolo is False:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.tremolo, value=0)
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[0], value=depth)
            )
        elif rate is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[1], value=rate)
            )

        wah, depth, rate = cp.wah(msg)
        if wah is True:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.sound_variation, value=127)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[2], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[3], value=rate)
            )
        elif wah is False:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.sound_variation, value=0)
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[2], value=depth)
            )
        elif rate is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[3], value=rate)
            )

        chorus, depth, speed = cp.chorus(msg)
        if chorus is True:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.chorus, value=127)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[4], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[5], value=speed)
            )
        elif chorus is False:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.chorus, value=0)
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[4], value=depth)
            )
        elif speed is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[5], value=speed)
            )

        phaser, depth, speed = cp.phaser(msg)
        if phaser is True:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.phaser, value=127)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[6], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[7], value=speed)
            )
        elif phaser is False:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.phaser, value=0)
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[6], value=depth)
            )
        elif speed is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[7], value=speed)
            )

        digital_delay, depth, time = cp.digital_delay(msg)
        if digital_delay is True:
            to_microtonOS.send(
                mido.Message(
                    "control_change", control=cc.effect_controller[0][0], value=127
                )
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[8], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[9], value=time)
            )
        elif digital_delay is False:
            to_microtonOS.send(
                mido.Message(
                    "control_change", control=cc.effect_controller[0][0], value=0
                )
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[8], value=depth)
            )
        elif time is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[9], value=time)
            )

        analog_delay, depth, time = cp.analog_delay(msg)
        if analog_delay is True:
            to_microtonOS.send(
                mido.Message(
                    "control_change", control=cc.effect_controller[1][0], value=127
                )
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[10], value=depth)
            )
            sleep(pause)
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[11], value=time)
            )
        elif analog_delay is False:
            to_microtonOS.send(
                mido.Message(
                    "control_change", control=cc.effect_controller[1][0], value=0
                )
            )
        elif depth is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[10], value=depth)
            )
        elif time is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.undefined[11], value=time)
            )

        reverb = cp.reverb(msg)
        if reverb is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=cc.reverb, value=reverb)
            )

        sustain = cp.sustain(msg)
        if sustain is not None:
            to_microtonOS.send(
                mido.Message("control_change", control=self.pedal, value=sustain)
            )

    def microtonOS(self, msg):
        to_reface_cp.send(msg)


to_microtonOS = Outport(client_name, name="microtonOS", verbose=False)
to_reface_cp = Outport(client_name, name="Reface CP", verbose=False)
script = Script()
from_reface_cp = Inport(script.reface_cp, client_name, name="Reface CP", verbose=False)
from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
make_threads([from_reface_cp.open, from_microtonOS.open])
