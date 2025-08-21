import time
from datetime import datetime
from loguru import logger
from sl_demo import Manager

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

    with Manager() as dev:
        dev.configuration()
        for i in range(3):
            dev.start_capture_th()
            while dev.get_capture_th_status():
                logger.info('in capture')
                time.sleep(1)
            dev.analyse_and_save()

if __name__ == '__main__':
    main()
