from src.sl_demo.analyser import Analyser


def main():
    # load from csv
    al = Analyser()
    al.set_digital_csv(
        digital_csv='output-2025-08-16_22-48-44/digital.csv',
    )



if __name__ == '__main__':
    main()
