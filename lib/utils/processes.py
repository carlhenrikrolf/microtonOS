# import mtsespy as esp
import signal
import sys
import time
import threading


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
        if hasattr(
            processes, "__len__"
        ):  # type(processes) is list or type(processes) is tuple:
            for process in processes:
                process.terminate()
        else:
            processes.terminate()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
