# from __future__ import print_function, unicode_literals
# from PyInquirer import prompt
#
# questions = [
#     {
#         'type': 'input',
#         'name': 'first_name',
#         'message': 'What\'s your first name',
#     },
#     {
#         'type': 'input',
#         'name': 'age',
#         'message': r"What's your age?",
#     }
# ]
#
# cli = [
#     {
#         'type': 'input',
#         'name': 'command',
#         'message': '>> poscli:'
#     }
# ]

from pydarknet import Detector

if __name__ == '__main__':
    Detector(
            bytes("./resources/darknet/coordinate.cfg", encoding="utf-8"),
            bytes("./resources/darknet/coordinate_70000.weights", encoding="utf-8"),
            0,
            bytes("./resources/darknet/coordinate.data", encoding="utf-8"),
        )
    # Detector(
    #     bytes("../darknet/test/cfg/red_circle.cfg", encoding="utf-8"),
    #     bytes("../darknet/test/cfg/obj.data", encoding="utf-8"),
    #     0,
    #     bytes("../darknet/backup/blue_circle_70000.weights", encoding="utf-8")
    # )
