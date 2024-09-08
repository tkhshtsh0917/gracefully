import sys
import signal
import time
from threading import Event, Thread

from gracefully.signal_handler import SignalHandler


WAIT_SECONDS_AFTER_SIGTERM = 25


def main(*args: Event) -> None:
    signal_received, process_finished = args

    while not signal_received.is_set():
        print("loop start")
        time.sleep(5)
        print("loop finish")

    # time.sleep(30)
    process_finished.set()


if __name__ == "__main__":
    signal_received = Event()
    process_finished = Event()

    handler = SignalHandler(
        signals=[signal.SIGTERM, signal.SIGINT],
        signal_received=signal_received,
        process_finished=process_finished,
        wait_seconds=WAIT_SECONDS_AFTER_SIGTERM,
        callbacks=[
            lambda: print("callback #1"),
            lambda: print("callback #2"),
            lambda: print("callback #3"),
        ],
    )

    Thread(target=main, args=[signal_received, process_finished], daemon=True).start()

    process_finished.wait()

    if handler.can_shutdown_gracefully:
        print("gracefully exit")
        sys.exit(0)
    else:
        print("force exit")
        sys.exit(1)
