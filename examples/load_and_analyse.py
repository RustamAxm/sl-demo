import os

from src.sl_demo.sl_demo import Manager
from loguru import logger

def main():
    # load special sale data
    with Manager() as dev:
        dev.load_capture(
            os.path.abspath('output-2025-08-16_22-48-44/example_capture.sal')
        )
        dev.analyse_and_save()

if __name__ == '__main__':
    main()
