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
        self.dataframe_dg = None
        self.dataframe_a = None
        self.dataframe_all = None

    def set_digital_csv(self, digital_csv):
        self.dataframe_dg = self.csv_operation(digital_csv)
        logger.debug(f"\n{self.dataframe_dg}")

    def set_analog_csv(self, analog_csv):
        self.dataframe_a = self.csv_operation(analog_csv)
        self.dataframe_a = self.dataframe_a.rename(columns={'Channel 0': "ChannelA 0"})
        logger.debug(f"\n{self.dataframe_a} \n{self.dataframe_a.columns}")

    @staticmethod
    def convert_to_datetime(dt_):
        return datetime.fromisoformat(dt_)

    def add_datetime_column(self, data):
        tmp = []
        for item in data['Time [s]']:
            delta = self.convert_to_datetime(item) - self.start_time
            tmp.append(delta)
        return tmp

    def csv_operation(self, file_csv):
        with open(file_csv, 'r') as f:
            dataframe = pd.read_csv(f)

        self.start_time = self.convert_to_datetime(dataframe['Time [s]'][0])
        logger.debug(f"{self.start_time=}, {type(self.start_time)}")
        tmp = self.add_datetime_column(dataframe)
        dataframe['delta_time'] = tmp
        return dataframe

    def merge_dataframes(self):
        self.dataframe_all = self.dataframe_a.merge(self.dataframe_dg, how='left', on='delta_time')
        logger.debug(f"\n{self.dataframe_all.head()}")
        logger.debug(f"{self.dataframe_all.columns}")
