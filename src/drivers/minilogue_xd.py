# internal modules
from utils import Outport, Inport, make_threads, load_config
from midi_implementation.midi1 import control_change as cc
from midi_implementation.korg import minilogue_xd as xd

# parameters
device_name = "Minilogue XD"
client_name = "Minilogue XD Driver"

# configurations
config = {
    "microtonOS": load_config(__file__, "../../config/microtonOS.toml"),
    "control_change": load_config(__file__, "../../config/control_change.toml"),
}
external_channel = config["microtonOS"]["Minilogue XD"]["channel"]
for i in range(16):
    if device_name == config["control_change"]["channel"][i]["device"]:
        internal_channel = i
received = config["control_change"]["channel"][internal_channel]["received"]


# definitions
class Script:
    def minilogue_xd(self, msg):
        if msg.type == "control_change":
            msg.channel = internal_channel
        to_microtonOS.send(msg)

    def microtonOS(self, msg):
        ignore = msg.type == "program_change"
        ignore = ignore or cc.is_in(msg, cc.bank_select)
        if not ignore:
            if msg.type == "control_change":
                if any(x.items() <= msg.dict().items() for x in received["CV in 1"]):
                    msg = xd.CVin1(
                        bimodal=False, value=msg.value, channel=external_channel
                    )
                if any(x.items() <= msg.dict().items() for x in received["CV in 2"]):
                    msg = xd.CVin2(
                        bimodal=False, value=msg.value, channel=external_channel
                    )
            elif hasattr(msg, "channel"):
                msg.channel = external_channel
            to_minilogue_xd.send(msg)


# run script
to_microtonOS = Outport(client_name, name="microtonOS")
to_minilogue_xd = Outport(client_name, name="Minilogue XD")
script = Script()
from_minilogue_xd = Inport(script.minilogue_xd, client_name, name="Minilogue XD")
from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
make_threads([from_minilogue_xd.open, from_microtonOS.open])
