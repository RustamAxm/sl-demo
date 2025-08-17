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



if __name__ == '__main__':
    main()
