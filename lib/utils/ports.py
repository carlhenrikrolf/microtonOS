import mido
import time


def is_expression(msg):
    if msg.type in ["aftertouch", "polytouch", "pitchwheel"]:
        return True
    elif msg.is_cc(74):
        return True
    else:
        return False


class Outport:
    def __init__(self, client_name, name=None, verbose=False):
        self.name = name
        self.verbose = verbose
        if self.name is None:
            self.output = mido.open_output(
                "from " + client_name, client_name=client_name
            )
        else:
            self.output = mido.open_output(
                self.name + " from " + client_name, client_name=client_name
            )

    def send(self, msg, seconds_between=0):
        messages = msg if hasattr("__len__") else [msg]
        for message in messages:
            self.output.send(message)
            if self.verbose and not is_expression(message):
                if self.name is None:
                    print("Send:", message)
                else:
                    print("Send (to " + self.name + "):", message)
            time.sleep(seconds_between)


class Inport:
    def __init__(self, process, client_name, name=None, verbose=False, length=None):
        self.process = process
        self.client_name = client_name
        self.name = name
        self.verbose = verbose
        self.length = length

    def open(self):
        if self.name is None:
            with mido.open_input(
                "to " + self.client_name, client_name=self.client_name
            ) as inport:
                if self.length is None:
                    for msg in inport:
                        if self.verbose and not is_expression(msg):
                            print("Receive:", msg)
                        self.process(msg)
                else:
                    pending = list(inport.iter_pending())
                    for i, msg in enumerate(pending):
                        if self.verbose and not is_expression(msg):
                            print("Receive:", msg)
                        if msg.type not in ["aftertouch", "polytouch"] and i < len(
                            pending
                        ):
                            self.process(msg)
                    time.sleep(self.length)
        else:
            with mido.open_input(
                self.name + " to " + self.client_name, client_name=self.client_name
            ) as inport:
                for msg in inport:
                    if self.length is None:
                        if self.verbose and not is_expression(msg):
                            print("Receive (from " + self.name + "):", msg)
                        self.process(msg)
                    else:
                        pending = list(inport.iter_pending())
                        for i, msg in enumerate(pending):
                            if self.verbose and not is_expression(msg):
                                print("Receive:", msg)
                            if msg.type not in ["aftertouch", "polytouch"] and i < len(
                                pending
                            ):
                                self.process(msg)
                        time.sleep(self.length)
