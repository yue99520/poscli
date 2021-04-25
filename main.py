from time import sleep

from PyInquirer import prompt

from app.interface import CommandLineRunner

if __name__ == '__main__':
    app = CommandLineRunner()
    app.start()

    cli = [
        {
            'type': 'input',
            'name': 'command',
            'message': 'poscli:~$'
        }
    ]
    while True:
        ipt = prompt(cli)
        if ipt['command'] == 'exit':
            break
