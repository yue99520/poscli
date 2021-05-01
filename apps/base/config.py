from configparser import ConfigParser, SectionProxy


class Configuration:

    @staticmethod
    def from_ini(ini='config.ini'):
        config_ini = ConfigParser()
        assert ini in config_ini.read(ini)

        return Configuration(config_ini)

    class System:
        def __init__(self, section: SectionProxy):
            self.log_level = section['LogLevel']
            self.show_detections_log = section['ShowDetectionsLog'] == "True"
            self.show_processed_log = section['ShowProcessedLog'] == "True"

    class Camera:
        def __init__(self, section: SectionProxy):
            self.vertical_camera_port = int(section['VerticalCameraPort'])

    class Coordinate:
        def __init__(self, section: SectionProxy):
            self.cfg_path = section['CfgPath']
            self.data_path = section['DataPath']
            self.weights_path = section['WeightsPath']
            self.confident_threshold = float(section['ConfidentThreshold'])

            self.real_origin_to_red_length = int(section['RealOriginToRedLength'])
            self.real_origin_to_blue_length = int(section['RealOriginToBlueLength'])

            self.origin_name = section['OriginName']
            self.red_name = section['RedName']
            self.blue_name = section['BlueName']

            self.manual_origin_x = int(section['ManualOriginX'])
            self.manual_origin_y = int(section['ManualOriginY'])
            self.manual_red_x = int(section['ManualRedX'])
            self.manual_red_y = int(section['ManualRedY'])
            self.manual_blue_x = int(section['ManualBlueX'])
            self.manual_blue_y = int(section['ManualBlueY'])

    class Target:
        def __init__(self, section: SectionProxy):
            self.cfg_path = section['CfgPath']
            self.data_path = section['DataPath']
            self.weights_path = section['WeightsPath']
            self.confident_threshold = float(section['ConfidentThreshold'])

    class Arm:
        def __init__(self, section: SectionProxy):
            self.destination_x = int(section['DestinationX'])
            self.destination_y = int(section['DestinationY'])
            self.destination_z = int(section['DestinationZ'])

            self.red_base = int(section['RedBase'])
            self.blue_base = int(section['BlueBase'])

            self.reset = section['Reset'] == "True"

    class View:
        def __init__(self, section: SectionProxy):
            self.buffer_length = int(section['BufferLength'])

    def __init__(self, config_ini: ConfigParser):
        self.system = self.System(config_ini['system'])
        self.camera = self.Camera(config_ini['camera'])
        self.coordinate = self.Coordinate(config_ini['coordinate'])
        self.target = self.Target(config_ini['target'])
        self.arm = self.Arm(config_ini['arm'])
        self.view = self.View(config_ini['view'])
