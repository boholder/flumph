import signal

from flumph.main_window import MainWindow


def signal_handler(signal, frame):
    print(' CTRL + C detected, exiting ...')
    exit(1)


if __name__ == '__main__':
    # CTRL+C signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    MainWindow().run()
