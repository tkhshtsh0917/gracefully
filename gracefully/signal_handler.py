from signal import signal, Signals
from threading import Event
from typing import Callable, Iterable


class SignalHandler:
    def __init__(
        self,
        signals: Iterable[Signals],
        signal_received: Event,
        process_finished: Event,
        wait_seconds: int,
        callbacks: Iterable[Callable] = [],
    ) -> None:
        for s in signals:
            signal(s, self.handle)

        self._signal_received = signal_received
        self._process_finished = process_finished
        self._wait_seconds = wait_seconds
        self._callbacks = callbacks

        self._can_shutdown_gracefully = True

    def handle(self, *args, **kwargs) -> None:
        print("Signal received. Preparing to shutdown...")
        self._signal_received.set()

        if not self._process_finished.wait(self._wait_seconds):
            print(f"{self._wait_seconds} seconds have passed. Force exit...")

            for callback in self._callbacks:
                callback()

            self._can_shutdown_gracefully = False
            self._process_finished.set()

    @property
    def can_shutdown_gracefully(self) -> bool:
        return self._can_shutdown_gracefully
