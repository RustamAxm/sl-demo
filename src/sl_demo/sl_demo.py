import os
import threading
from datetime import datetime

from loguru import logger
from saleae import automation


class Manager:
    def __init__(self):
        self.manager = automation.Manager.connect(port=10430)
        self.device_id = "F4243" #'A7D1BB81883C0092'

    def close(self):
        self.manager.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def configuration(
            self,
            enabled_digital_channels=[0, 2],
            digital_sample_rate=1_000_000,
            duration_seconds=5.0,
    ):
        """
        Configure the capturing device to record on digital channels 0, 1, 2, and 3,
        with a sampling rate of 10 MSa/s, and a logic level of 3.3V.
        The settings chosen here will depend on your device's capabilities and what
        you can configure in the Logic 2 UI.
        :return:
        """
        logger.debug(f"{duration_seconds=}")
        self.device_configuration = automation.LogicDeviceConfiguration(
            enabled_digital_channels=enabled_digital_channels,
            digital_sample_rate=digital_sample_rate,
        )
        # Record 5 seconds of data before stopping the capture
        self.capture_configuration = automation.CaptureConfiguration(
            capture_mode=automation.TimedCaptureMode(duration_seconds=duration_seconds)
        )

    def start_capture_th(self):
        self.th = threading.Thread(target=self._start_capture, daemon=False)
        self.th.start()

    def get_capture_th_status(self):
        if self.th.is_alive():
            return True
        else:
            self.th.join()
            return False

    def _start_capture(self):
        """
        Start a capture - the capture will be automatically closed when leaving the `with` block
        Note: The serial number 'F4241' is for the Logic Pro 16 demo device.
              To use a real device, you can:
                1. Omit the `device_id` argument. Logic 2 will choose the first real (non-simulated) device.
                2. Use the serial number for your device. See the "Finding the Serial Number
                   of a Device" section for information on finding your device's serial number.
        :return:
        """

        logger.info('start capture')
        self.capture =  self.manager.start_capture(
                device_id=self.device_id,
                device_configuration=self.device_configuration,
                capture_configuration=self.capture_configuration)

            # Wait until the capture has finished
            # This will take about 5 seconds because we are using a timed capture mode
        self.capture.wait()
        logger.debug(f'capture done {self.capture}')

    def analyse_and_save(self):
        """
        Add an analyzer to the capture
        Note: The simulator output is not actual Serial data
        :return:
        """

        serial_analyzer = self.capture.add_analyzer(
            'Async Serial',
            label=f'Test Analyzer',
            settings={
                'Input Channel': 2,
                'Bit Rate (Bits/s)': 115200,
                'Bits per Frame': '8 Bits per Transfer (Standard)',
            }
        )

        # Store output in a timestamped directory
        output_dir = os.path.join(os.getcwd(), f'output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
        os.makedirs(output_dir)

        # Export raw digital data to a CSV file
        self.capture.export_raw_data_csv(
            directory=output_dir,
            digital_channels=[0, 2],
            iso8601_timestamp=True,
        )
        logger.info(f'Export raw digital data to a CSV file {output_dir=}')
        # Export analyzer data to a CSV file
        analyzer_export_filepath = os.path.join(output_dir, 'serial_export.csv')
        self.capture.export_data_table(
            filepath=analyzer_export_filepath,
            analyzers=[serial_analyzer]
        )
        logger.info(f'Export analyzer data to a CSV file {analyzer_export_filepath=}')

        # Finally, save the capture to a file
        capture_filepath = os.path.join(output_dir, 'example_capture.sal')
        self.capture.save_capture(filepath=capture_filepath)
        logger.info(f'Finally, save the capture to a file {capture_filepath=}')

        self.capture.close()
        self.capture = None

    def load_capture(self, file_path):
        if not os.path.isabs(file_path):
            raise ValueError(f"not full path {file_path=}")
        if file_path.endswith('sal'):
            self.capture = self.manager.load_capture(file_path)
