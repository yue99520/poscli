from copy import copy
from threading import Lock


class SystemState:
    INITIALIZING = 1
    PAUSE = 0
    RUNNING = 2
    EXIT = -1

    def __init__(self):
        self.state = SystemState.INITIALIZING
        self.lock = Lock()

    def get_state(self):
        self.lock.acquire()
        state = copy(self.state)
        self.lock.release()
        return state

    def set_state(self, state):
        self.lock.acquire()
        self.state = state
        self.lock.release()