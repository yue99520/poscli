from apps.base.config import Configuration
from apps.context import SystemContext
from PyInquirer import prompt


class CommandController:
    cli = [
        {
            'type': 'input',
            'name': 'command',
            'message': '~poscli$'
        }
    ]

    def __init__(self, config: Configuration, context: SystemContext):
        self.config = config
        self.context = context

    def run(self):
        while True:
            cmd = prompt(CommandController.cli)
            if str(cmd['command']).strip() == 'exit':
                print('exiting...')
                self.context.stop_all()
                print('exited')
