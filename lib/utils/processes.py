import mtsespy as esp
import signal
import sys
import time
import threading

class Warmup:
    message = "microtonOS is warming up ..."

    def master(self):
        if esp.has_ipc() and not esp.can_register_master():
            esp.reinitialize()

    def client(self):
        for _ in range(60):
            if esp.can_register_master():
                time.sleep(1)
            else:
                break
                
warmup = Warmup()

def make_threads(functions, args=None):
    n = len(functions)
    args = [()] * n if args is None else args
    threads = [None] * n
    for i in range(n):
        threads[i] = threading.Thread(target=functions[i], args=args[i], daemon=True)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def handle_terminations(processes):
    def signal_handler(signum, frame):
        if type(processes) is list or type(processes) is tuple:
            for process in processes:
                process.terminate()
        else:
            processes.terminate()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)

