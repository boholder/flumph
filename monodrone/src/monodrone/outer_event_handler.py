import queue
from enum import IntEnum
from typing import Any

from duodrone.data import OuterEvent


class Priority(IntEnum):
    HIGH = 0,
    MIDDLE = 1,
    LOW = 2


class OuterEventHandler:
    __instance: 'OuterEventHandler' = None
    __queue = queue.PriorityQueue()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(OuterEventHandler, cls).__new__(cls)
        return cls.__instance

    def get(self) -> Any | None:
        try:
            t = self.__queue.get(block=False)
            return t[1]
        except queue.Empty:
            return None

    def put(self, priority: int, event):
        self.__queue.put((priority, event))

    def handle(self, event: OuterEvent):
        self.put(Priority.MIDDLE, event.text)
