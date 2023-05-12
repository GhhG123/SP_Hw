import threading


class Timer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.timer = None
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.callback()

    def start(self):
        if not self.is_running:
            self.timer = threading.Timer(self.interval, self._run)
            self.timer.start()
            self.is_running = True

    def cancel(self):
        self.timer.cancel()
        self.is_running = False
