from matplotlib import pyplot as plt

from src.sl_demo.analyser import Analyser


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
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time [s]'], df['ChannelA 0'], label='D', marker='o', linestyle='-', color='red')
    plt.plot(df['Time [s]'], df['Channel 0'], label='A', marker='s', linestyle='--', color='blue')
    plt.title('График данных')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
