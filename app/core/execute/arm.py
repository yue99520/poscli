from threading import Thread


class ArmService(Thread):
    def __init__(self):
        super().__init__(name="ArmService")

    def run(self) -> None:
        pass
