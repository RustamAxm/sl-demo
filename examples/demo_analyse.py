import datetime

import yaml
from loguru import logger
from matplotlib import pyplot as plt

from src.sl_demo.analyser import Analyser

def plot_df(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time [s]'], df['ChannelA 0'],
             label='D', marker='o', linestyle='-', color='red')
    plt.plot(df['Time [s]'], df['Channel 0'],
             label='A', marker='s', linestyle='--', color='blue')
    plt.title('График данных')
    plt.grid(True)
    plt.show()


def check_signals(to_check, exp_start='', ref_item={}):
    start = datetime.datetime.fromisoformat(exp_start)
    to_check = datetime.datetime.fromisoformat(to_check)
    logger.debug(f"{to_check - start}")

    min_ = datetime.timedelta(microseconds=ref_item['min']) + start
    max_ = datetime.timedelta(microseconds=ref_item['max'])  + start
    if min_ < to_check < max_:
        logger.debug('True')
    else:
        logger.debug(f"False")


def main():
    # load from csv
    al = Analyser()
    al.set_digital_csv(
        digital_csv='output-2025-08-17_11-00-01/digital.csv',
    )
    al.set_analog_csv(
        analog_csv='output-2025-08-17_11-00-01/analog.csv'
    )
    al.merge_dataframes()

    # df = al.get_all_dataframe_resample()
    # plot_df(df)
    start = '2025-08-17T07:59:59.899+00:00'
    end = '2025-08-17T07:59:59.8995000+00:00'
    end = datetime.datetime.fromisoformat(end)
    logger.info(f"{al.get_filtered_time(start, end)}")

    first_r = al.get_first_digital_rising()
    logger.info(f"{first_r=}")
    with open('digital_signals.yaml', 'r') as f:
        config = yaml.safe_load(f)
    for item in config['channels']:
        check_signals(
            to_check=first_r,
            exp_start='2025-08-17T07:59:59.829076240+00:00',
            ref_item=item,
        )


if __name__ == '__main__':
    main()
