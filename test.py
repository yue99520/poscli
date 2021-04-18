from __future__ import print_function, unicode_literals
from PyInquirer import prompt

questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    },
    {
        'type': 'input',
        'name': 'age',
        'message': r"What's your age?",
    }
]

cli = [
    {
        'type': 'input',
        'name': 'command',
        'message': '>> poscli:'
    }
]

if __name__ == '__main__':
    while True:
        ans = prompt(cli)
        print(ans)
