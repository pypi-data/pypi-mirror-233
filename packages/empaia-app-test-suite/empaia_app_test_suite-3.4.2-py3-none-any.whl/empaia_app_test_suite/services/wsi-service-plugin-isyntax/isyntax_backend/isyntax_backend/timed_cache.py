import threading
import time


class TimedCache:
    def __init__(self, timeout_seconds, callback_kill_proc):
        self.cache = {}
        self.cleanup_interval = 10
        self.running = True

        self.timeout_seconds = timeout_seconds

        self.semaphore = threading.Semaphore()
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_thread, args=(self.semaphore, callback_kill_proc)
        )
        self.cleanup_thread.start()

    def set(self, key, value):
        with self.semaphore:
            self.cache[key] = {
                "value": value,
                "expiration_time": time.time() + self.timeout_seconds,
            }

    def get(self, key, default=None):
        with self.semaphore:
            item = self.cache.get(key)
            if item:
                now = time.time()
                if now < item["expiration_time"]:
                    item["expiration_time"] = now + self.timeout_seconds
                    return item["value"]
                else:
                    del self.cache[key]
        return default

    def _cleanup_thread(self, semaphore, callback_kill_proc):
        while self.running:
            with semaphore:
                self._cleanup_expired_items(callback_kill_proc=callback_kill_proc)
            time.sleep(self.cleanup_interval)

    def _cleanup_expired_items(self, callback_kill_proc):
        expired_items = {
            k: v for (k, v) in self.cache.items() if time.time() >= v["expiration_time"]
        }
        for exp_key, exp_item in expired_items.items():
            callback_kill_proc(exp_item["value"])
            del self.cache[exp_key]

    def stop(self):
        self.running = False
        self.cleanup_thread.join()
