import datetime

import yaml
from loguru import logger
from matplotlib import pyplot as plt

from src.sl_demo.analyser import Analyser

def plot_df(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time [s]'], df['AChannel 0'],
             label='D', marker='o', linestyle='-', color='red')
    plt.plot(df['Time [s]'], df['Channel 0'],
             label='A', marker='s', linestyle='--', color='blue')
    plt.title('График данных')
    plt.grid(True)
    plt.show()


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

    df = al.get_all_dataframe_resample()
    plot_df(df)
    start = '2025-08-17T07:59:59.899+00:00'
    end = '2025-08-17T07:59:59.8995000+00:00'
    end = datetime.datetime.fromisoformat(end)
    logger.info(f"{al.get_filtered_time(start, end)}")


    with open('digital_signals.yaml', 'r') as f:
        config = yaml.safe_load(f)

    exp_start = '2025-08-17T07:59:59.829076240+00:00'
    for item in config['channels']:
        try:
            first_r = al.get_first_digital_rising(
                ch_id=item['name']
            )
        except Exception as ex:
            logger.warning(f'{ex=}')
            continue
        logger.info(f"{first_r=}")
        al.check_signals(
            to_check=first_r,
            experiment_start=exp_start,
            ref_item=item,
        )


if __name__ == '__main__':
    main()
