import os
import time
from datetime import datetime
from loguru import logger
from sl_demo import Manager
from src.sl_demo.analyser import Analyser


@logger.catch
def main():
    """
    # Connect to the running Logic 2 Application on port `10430`.
    # Alternatively you can use automation.Manager.launch() to launch a new Logic 2 process - see
    # the API documentation for more details.
    # Using the `with` statement will automatically call manager.close() when exiting the scope. If you
    # want to use `automation.Manager` outside of a `with` block, you will need to call `manager.close()` manually.
    :return:
    """

    logger.add(f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    logger.info("start connection")
    iter = 1
    # demo get vals
    with Manager() as dev:
        for i in range(3):
            dev.configuration(
                duration_seconds=iter,
            )
            iter += 1
            dev.start_capture_th()
            while dev.get_capture_th_status():
                logger.info('in capture')
                time.sleep(0.2)
            dev.analyse_and_save()
    # load from csv
    al = Analyser()
    al.set_digital_csv(
        digital_csv='output-2025-08-16_22-24-12/digital.csv',
    )
    # load special sale data
    dev = Manager()
    dev.load_capture(
        os.path.abspath('output-2025-08-16_22-24-12/example_capture.sal')
    )
    dev.analyse_and_save()
    dev.close()


if __name__ == '__main__':
    main()
