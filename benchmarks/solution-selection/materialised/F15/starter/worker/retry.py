from worker.errors import PermanentFailure, TransientFailure

IDLE = "IDLE"
SENDING = "SENDING"
BACKOFF = "BACKOFF"
SUCCEEDED = "SUCCEEDED"
FAILED_PERMANENT = "FAILED_PERMANENT"
EXHAUSTED = "EXHAUSTED"


class RetryMachine:
    def __init__(self, tracer, clock, max_attempts=4, delay=1.0):
        self.tracer = tracer
        self.clock = clock
        self.max_attempts = max_attempts
        self.delay = delay

    def run(self, operation):
        state = IDLE
        attempt = 0
        self.tracer.span("retry.transition", source=IDLE, target=SENDING, attempt=attempt + 1)
        state = SENDING
        while True:
            if state == SENDING:
                attempt = attempt + 1
                try:
                    operation()
                    self.tracer.span("retry.transition", source=SENDING, target=SUCCEEDED, attempt=attempt)
                    state = SUCCEEDED
                    return state
                except PermanentFailure:
                    self.tracer.span("retry.transition", source=SENDING, target=FAILED_PERMANENT, attempt=attempt)
                    state = FAILED_PERMANENT
                    return state
                except TransientFailure:
                    if attempt >= self.max_attempts:
                        self.tracer.span("retry.transition", source=SENDING, target=EXHAUSTED, attempt=attempt)
                        state = EXHAUSTED
                        return state
                    else:
                        self.tracer.span("retry.transition", source=SENDING, target=BACKOFF, attempt=attempt)
                        state = BACKOFF
            elif state == BACKOFF:
                self.clock.sleep(self.delay)
                self.tracer.span("retry.transition", source=BACKOFF, target=SENDING, attempt=attempt + 1)
                state = SENDING
