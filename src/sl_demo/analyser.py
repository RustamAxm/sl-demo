import pandas as pd

class Analyser:
    def __init__(self):
        pass

    def set_digital_csv(self, digital_csv):
        with open(digital_csv, 'r') as f:
            data = pd.read_csv(f)

        print(data)
