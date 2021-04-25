import configparser


class Configuration:

    @staticmethod
    def from_ini(ini='config.ini'):
        config_ini = configparser.ConfigParser()
        assert ini in config_ini.read(ini)

        config = Configuration()

        section = 'system'
        config.system.log_level = config_ini[section]['LogLevel']

        section = 'camera'
        config.camera.vertical_camera_port = int(config_ini[section]['VerticalCameraPort'])

        section = 'coordinate'
        config.coordinate.cfg_path = config_ini[section]['CfgPath']
        config.coordinate.data_path = config_ini[section]['DataPath']
        config.coordinate.weights_path = config_ini[section]['WeightsPath']
        config.coordinate.confident_threshold = int(config_ini[section]['ConfidentThreshold'])

        config.coordinate.real_origin_to_red_length = int(config_ini[section]['RealOriginToRedLength'])
        config.coordinate.real_origin_to_blue_length = int(config_ini[section]['RealOriginToBlueLength'])

        config.coordinate.origin_name = config_ini[section]['OriginName']
        config.coordinate.red_name = config_ini[section]['RedName']
        config.coordinate.blue_name = config_ini[section]['BlueName']

        config.coordinate.manual_origin_x = int(config_ini[section]['ManualOriginX'])
        config.coordinate.manual_origin_y = int(config_ini[section]['ManualOriginY'])

        config.coordinate.manual_red_x = int(config_ini[section]['ManualRedX'])
        config.coordinate.manual_red_y = int(config_ini[section]['ManualRedY'])

        config.coordinate.manual_blue_x = int(config_ini[section]['ManualBlueX'])
        config.coordinate.manual_blue_y = int(config_ini[section]['ManualBlueY'])

        section = 'target'
        config.target.cfg_path = config_ini[section]['CfgPath']
        config.target.data_path = config_ini[section]['DataPath']
        config.target.weights_path = config_ini[section]['WeightsPath']
        config.target.confident_threshold = int(config_ini[section]['ConfidentThreshold'])

        section = 'arm'
        config.arm.destination_x = int(config_ini[section]['DestinationX'])
        config.arm.destination_Y = int(config_ini[section]['DestinationY'])
        config.arm.destination_Z = int(config_ini[section]['DestinationZ'])
        config.arm.vertical_off_set = int(config_ini[section]['VerticalOffSet'])
        config.arm.horizontal_off_set = int(config_ini[section]['HorizontalOffSet'])

    class System:
        def __init__(self):
            self.log_level = None

    class Camera:
        def __init__(self):
            self.vertical_camera_port = None

    class Coordinate:
        def __init__(self):
            self.cfg_path = None
            self.data_path = None
            self.weights_path = None
            self.confident_threshold = None

            self.real_origin_to_red_length = None
            self.real_origin_to_blue_length = None

            self.origin_name = None
            self.red_name = None
            self.blue_name = None

            self.manual_origin_x = None
            self.manual_origin_y = None
            self.manual_red_x = None
            self.manual_red_y = None
            self.manual_blue_x = None
            self.manual_blue_y = None

    class Target:
        def __init__(self):
            self.cfg_path = None
            self.data_path = None
            self.weights_path = None
            self.confident_threshold = None

    class Arm:
        def __init__(self):
            self.destination_x = None
            self.destination_y = None
            self.destination_z = None

            self.vertical_off_set = None
            self.horizontal_off_set = None

    def __init__(self):
        self.system = self.System()
        self.camera = self.Camera()
        self.coordinate = self.Coordinate()
        self.target = self.Target()
        self.arm = self.Arm()
