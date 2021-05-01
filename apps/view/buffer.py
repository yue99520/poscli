class ViewBuffer:
    def __init__(self, buffer_length):
        self.buffer_counter = 0
        self.buffer_length = buffer_length
        self.source = None

    def buffer(self, source):
        self.buffer_counter += 1
        if self.source is None or self.should_refresh():
            self.source = source
            self.buffer_counter = 0
        return self.source

    def should_refresh(self) -> bool:
        return self.buffer_counter >= self.buffer_length

    def _get_source(self) -> list:
        pass
