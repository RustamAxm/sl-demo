from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from loguru import logger


@dataclass
class Range:
    min_: str
    max_: str


@dataclass
class Timings:
    ch0 = Range(min_=0, max_=1)
    ch1 = Range(min_=0, max_=1)


class Analyser:
    def __init__(self):
        self.start_time = None

    def set_digital_csv(self, digital_csv):
        with open(digital_csv, 'r') as f:
            data = pd.read_csv(f)

        self.start_time = datetime.fromisoformat(data['Time [s]'][0])
        logger.debug(f"{self.start_time=}, {type(self.start_time)}")
        logger.debug(self.start_time > datetime.fromisoformat(data['Time [s]'][1]))
