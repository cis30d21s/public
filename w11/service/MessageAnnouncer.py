from typing import Optional
import queue
import logging


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self) -> queue.Queue:
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, message: str, event: Optional[str] = None):
        logging.debug(f'Announcing `{event}` message: {message}')
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(self._format_sse(message, event))
            except queue.Full:
                del self.listeners[i]

    @staticmethod
    def _format_sse(data: str, event: Optional[str] = None) -> str:
        message = f'data: {data}\n\n'
        if event:
            message = f'event: {event}\n{message}'
        return message
