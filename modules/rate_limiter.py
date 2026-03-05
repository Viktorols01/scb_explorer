import time


class RateLimiter:
    def __init__(self, token_capacity, token_refill_count, refill_time):
        self.token_capacity = token_capacity
        self.token_refill_count = token_refill_count
        self.refill_time = refill_time

        self.tokens = token_capacity

        self.last_refill_time = time.time()

    def acquire(self, tokens):
        while self.tokens < tokens:
            time_since_last_refill = time.time() - self.last_refill_time
            time_until_refill = self.refill_time - time_since_last_refill
            if time_until_refill > 0:
                time.sleep(time_until_refill)
            self._add_pending_tokens()

        self.tokens -= tokens

    def _add_pending_tokens(self):
        time_since_last_refill = time.time() - self.last_refill_time
        refill_count = time_since_last_refill // self.refill_time
        refill_overtime = time_since_last_refill % self.refill_time
        self.last_refill_time = time.time() - refill_overtime
        self.tokens += self.token_refill_count*refill_count
        if self.tokens > self.token_capacity:
            self.tokens = self.token_capacity