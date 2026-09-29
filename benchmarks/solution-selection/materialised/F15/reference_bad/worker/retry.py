class RetryMachine:
    def __init__(self, tracer, clock, max_attempts=4, delay=1.0):
        self.tracer, self.clock, self.max_attempts, self.delay = tracer, clock, max_attempts, delay

    def run(self, operation):
        while True:
            try:
                operation(); return "SUCCEEDED"
            except Exception:
                self.clock.sleep(self.delay)
