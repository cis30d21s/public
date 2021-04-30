from typing import Optional, Tuple
import queue
import logging


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []
        self.id_counter = 0

    def listen(self) -> Tuple[int, queue.Queue]:
        q = queue.Queue(maxsize=5)
        if len(self.listeners) > 5:
            del self.listeners[0]
        self.id_counter += 1
        self.listeners.append((self.id_counter, q))
        count = len(self.listeners)
        logging.debug(
            f'{count} listeners, new listener #{self.id_counter}')
        # say hi to confirm connection
        logging.debug(f'Saying hi to listener #{self.id_counter}')
        q.put_nowait(self._format_sse('hi'))
        return self.id_counter, q

    def announce(self, message: str, event: Optional[str] = None):
        logging.debug(f'Announcing `{event}` message: {message}')
        for listener in reversed(self.listeners):
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
