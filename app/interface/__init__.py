from subprocess import Popen, PIPE, STDOUT

from threading import Thread


class CommandLineRunner(Thread):
    def run(self) -> None:
        while True:
            print('ok')
