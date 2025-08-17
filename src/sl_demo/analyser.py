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

    def add_timedelta_column(self, data):
        tmp = pd.to_datetime(data['Time [s]']) - self.start_time
        return tmp

    def csv_operation(self, file_csv):
        with open(file_csv, 'r') as f:
            dataframe = pd.read_csv(f)

        self.start_time = self.convert_to_datetime(dataframe['Time [s]'][0])
        logger.debug(f"{self.start_time=}, {type(self.start_time)}")
        # tmp = self.add_timedelta_column(dataframe)
        # dataframe['delta_time'] = tmp
        return dataframe

    def merge_dataframes(self):
        dataframe_a = self.dataframe_a.set_index('Time [s]')
        dataframe_dg = self.dataframe_dg.set_index('Time [s]')
        self.dataframe_all = pd.concat(
            [dataframe_a, dataframe_dg],
            axis=1,
            sort=True,
        )
        self.dataframe_all = (self.dataframe_all.
                              reset_index().
                              rename(columns={'index': 'Time [s]'}).
                              ffill())
        self.dataframe_all['Time [s]'] = pd.to_datetime(self.dataframe_all['Time [s]'])
        logger.debug(f"\n{self.dataframe_all.head()}")
        logger.debug(f"{self.dataframe_all.columns}")

    def get_all_dataframe_resample(self, resample_time='1ms'):
        tmp = self.dataframe_all.set_index('Time [s]')
        tmp = tmp.resample(resample_time).mean()
        return tmp.reset_index()

    def get_filtered_time(self, start, end):
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        tmp = self.dataframe_all.set_index('Time [s]')
        filtered_df = tmp.loc[start: end]
        return filtered_df

    def get_first_digital_rising(self, ch_id='Channel 0'):
        df = self.dataframe_dg
        first_rise = df[df[ch_id] == 1].index[0]
        return df.loc[first_rise, 'Time [s]']