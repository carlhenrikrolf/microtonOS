# internal modules
from utils import Outport, Inport, make_threads, load_config
from midi_implementation.midi1 import control_change as cc
from midi_implementation.korg import minilogue_xd as xd

# parameters
device_name = "Minilogue XD"
client_name = "Minilogue XD Driver"

# configurations
config = {
    "general_settings": load_config(__file__, "../../config/general_settings.toml"),
    "control_change": load_config(__file__, "../../config/control_change.toml"),
}
external_channel = config["general_settings"][device_name]["channel"]
for i in range(16):
    if device_name == config["control_change"]["channel"][i]["device"]:
        internal_channel = i
received = config["control_change"]["channel"][internal_channel]["received"]


# definitions
class Script:
    def __init__(self):
        self.is_local = False

    def minilogue_xd(self, msg):
        if not self.is_local and msg.type in [
            "control_change",
            "program_change",
            "sysex",
        ]:
            to_minilogue_xd.send(msg)
        if msg.type == "clock":
            to_clock.send(msg)
        elif msg.type == "control_change":
            if xd.is_continuous(msg):
                to_microtonOS.send(msg.copy(channel=internal_channel))
        else:
            to_microtonOS.send(msg)

    def microtonOS(self, msg):
        ignore = msg.type == "program_change"
        ignore |= cc.is_in(msg, cc.bank_select)
        ignore |= msg.type == "control_change" and msg.channel == internal_channel
        if not ignore:
            if msg.type == "control_change":
                if any(x.items() <= msg.dict().items() for x in received["CVin1"]):
                    msg = xd.CVin1(
                        bimodal=True, value=msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CVin2"]):
                    msg = xd.CVin2(
                        bimodal=True, value=msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CVin1+"]):
                    msg = xd.CVin1(
                        bimodal=False, value=msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CVin2+"]):
                    msg = xd.CVin2(
                        bimodal=False, value=msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CVin1-"]):
                    msg = xd.CVin1(
                        bimodal=False, value=-msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CVin2-"]):
                    msg = xd.CVin2(
                        bimodal=False, value=-msg.value, channel=external_channel
                    )
                if msg.is_cc(cc.local_onoff_switch):
                    self.is_local = True if msg.value >= 64 else False
                    print("local", self.is_local)
            elif hasattr(msg, "channel"):
                msg.channel = external_channel
            to_minilogue_xd.send(msg)


# run script
to_microtonOS = Outport(client_name, name="microtonOS")
to_minilogue_xd = Outport(client_name, name="Minilogue XD")
to_clock = Outport(client_name, name="Clock")
script = Script()
from_minilogue_xd = Inport(script.minilogue_xd, client_name, name="Minilogue XD")
from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
make_threads([from_minilogue_xd.open, from_microtonOS.open])
