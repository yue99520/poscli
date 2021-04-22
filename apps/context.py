class SystemContext:
    def __init__(self):
        self.coordinate_detect_thread = None
        self.target_detect_thread = None
        self.process_thread = None
        self.arm_thread = None
        self.view_thread = None
