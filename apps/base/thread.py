import abc
from threading import Thread, Lock

from apps.base.config import Configuration
from apps.context import SystemContext


class SystemState:
    """
    線程安全的系統狀態
    """
    STOPPED = 0
    INITIALIZING = 1
    INITIALIZED = -1
    RUNNING = 2
    STOPPING = 3

    def __init__(self):
        self.state = SystemState.INITIALIZING
        self.lock = Lock()

    def get_state(self):
        self.lock.acquire()
        state = self.state
        self.lock.release()
        return state

    def set_state(self, state):
        self.lock.acquire()
        self.state = state
        self.lock.release()


class BaseThread(Thread, abc.ABC):
    """
    可控生命週期線程物件
    """
    def __init__(self, name: str):
        super(BaseThread, self).__init__(name=name)
        self.thread_state = SystemState()
        self.thread_state.set_state(SystemState.INITIALIZING)

    def start(self) -> None:
        self.thread_state.set_state(SystemState.RUNNING)
        super(BaseThread, self).start()

    def stop(self, wait=False):
        self.thread_state.set_state(SystemState.STOPPING)
        while wait:
            if self.thread_state.get_state() is SystemState.STOPPED:
                break

    def run(self) -> None:
        while True:
            if self.thread_state.get_state() is SystemState.STOPPING:
                self.stopping()
                break
            self.run_loop()

    def stopping(self):
        self.thread_state.set_state(SystemState.STOPPED)

    def run_loop(self) -> None:
        raise NotImplementedError()


class ContextThread(BaseThread):
    def __init__(self, name: str, context: SystemContext):
        super().__init__(name)
        self.context: SystemContext = context


class ApplicationThread(ContextThread):
    def __init__(self, name: str, context: SystemContext, config: Configuration):
        super().__init__(name, context)
        self.configuration = config
