import os
import time
from datetime import datetime
from loguru import logger
from sl_demo import Manager

@logger.catch
def main():

    logger.add(f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    logger.info("start connection")
    iter = 1
    # demo get vals
    with Manager() as dev:
        for i in range(1):
            dev.configuration(
                duration_seconds=iter,
            )
            iter += 1
            dev.start_capture_th()
            while dev.get_capture_th_status():
                logger.info('in capture')
                time.sleep(0.2)
            dev.analyse_and_save()



if __name__ == '__main__':
    main()
