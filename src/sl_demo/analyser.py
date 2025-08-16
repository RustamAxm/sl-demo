from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from loguru import logger


@dataclass
class Range:
    min_: datetime
    max_: datetime


@dataclass
class Timings:
    ch0 = Range(min_=0, max_=1)
    ch1 = Range(min_=0, max_=1)


class Analyser:
    def __init__(self):
        self.start_time = None
        self.dataframe = None

    def set_digital_csv(self, digital_csv):
        with open(digital_csv, 'r') as f:
            dataframe = pd.read_csv(f)

        self.start_time = self.convert_to_datetime(dataframe['Time [s]'][0])
        logger.debug(f"{self.start_time=}, {type(self.start_time)}")
        logger.debug(self.start_time > datetime.fromisoformat(dataframe['Time [s]'][1]))
        tmp = self.add_datetime_column(dataframe)
        dataframe['delta_time'] = tmp
        self.dataframe = dataframe
        logger.debug(f"\n{dataframe}")

    @staticmethod
    def convert_to_datetime(dt_):
        return datetime.fromisoformat(dt_)

    def add_datetime_column(self, data):
        tmp = []
        for item in data['Time [s]']:
            delta = self.convert_to_datetime(item) - self.start_time
            tmp.append(delta)
        logger.debug(f"{tmp=}")
        return tmp
