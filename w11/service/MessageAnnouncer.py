from typing import Optional, Tuple
import queue
import threading
import logging

# shared among threads
_listeners = []


class MessageAnnouncer:

    def __init__(self):
        self.id_counter = 0
        self._lock = threading.RLock()

    def listen(self) -> Tuple[int, queue.Queue]:
        global _listeners  # ensure changes to visible to all threads
        with self._lock:
            q = queue.Queue(maxsize=5)
            if len(_listeners) > 5:
                del _listeners[0]
            self.id_counter += 1
            _listeners.append((self.id_counter, q))
            count = len(_listeners)
            logging.debug(
                f'{count} listeners, new listener #{self.id_counter}')
            # say hi to confirm connection
            logging.debug(f'Saying hi to listener #{self.id_counter}')
            q.put_nowait(self._format_sse('hi'))
        return self.id_counter, q

    def announce(self, message: str, event: Optional[str] = None):
        global _listeners
        with self._lock:
            logging.debug(
                f'Announcing `{event}` message: {message} to {len(_listeners)} listeners')
            for listener in reversed(_listeners):
                try:
                    listener[1].put_nowait(self._format_sse(message, event))
                    logging.debug(f'Ready for listener #{listener[0]}')
                except queue.Full:
                    try:
                        logging.debug(
                            f'Dropping message for listener {listener[0]}')
                        listener[1].get_nowait()
                    except queue.Empty:
                        ...

    @staticmethod
    def _format_sse(data: str, event: Optional[str] = None) -> str:
        message = f'data: {data}\n\n'
        if event:
            message = f'event: {event}\n{message}'
        return message
