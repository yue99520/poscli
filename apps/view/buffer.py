class ViewBuffer:
    def __init__(self, buffer_length):
        self.buffer_counter = 0
        self.buffer_length = buffer_length
        self.source = None

    def buffer(self):
        self.buffer_counter += 1
        if self.source is None or self.should_refresh():
            self.source = self._get_source()
            self.buffer_counter = 0
        return self.source

    def should_refresh(self) -> bool:
        return self.buffer_counter >= self.buffer_length

    def _get_source(self) -> list:
        pass


class PositionsSource(ViewBuffer):
    def __init__(self, buffer_length, detection_thread):
        super().__init__(buffer_length)
        self.thread = detection_thread

    def _get_source(self) -> list:
        return self.thread.get_unfiltered_positions(peak=True)
