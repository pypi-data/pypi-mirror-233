"""
CSV file processor. Reads CSV files and writes to CSV files.
"""
import csv
from abc import ABC, abstractmethod
from lottostar.app.config.main import settings
from lottostar.app.tickets.main import Ticket
from .file_locator import FileLocator


# pylint: disable=too-few-public-methods
class AbstractCsvProcessor(ABC):
    """
    Abstract CSV processor
    """
    def __init__(self, file: FileLocator, ticket: Ticket = None) -> None:
        self.file = file
        self.ticket = ticket

    @abstractmethod
    def process(self):
        """
        Process the CSV file
        """
        pass  # pylint: disable=unnecessary-pass


# pylint: disable=too-few-public-methods
class WinningEntryCsvProcessor(AbstractCsvProcessor):
    """
    Input CSV file processor
    """
    def process(self) -> str:
        """
        Process the CSV file
        """
        with open(self.file.get_results_file_path(),
                  "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            # skip to where the winning entry numbers are
            data_row = next(
                row for row_index, row in enumerate(csv_reader, start=1) if
                row_index == settings.WINNING_ENTRY_DATA_ROW
            )
            return data_row[0]


class OutputCsvProcessor(AbstractCsvProcessor):
    """
    Process output csv file with:
    1. Count of matched numbers
    2. Count of matched numbers
    3. If a Ticket has matched all numbers,
    indicate that the jackpot was won
    """
    def process(self) -> None:
        """
        Process the CSV file
        """
        with open(self.file.get_entry_tickets_file_path(),
                  mode='r', newline='', encoding="utf-8") as input_file:
            # read the input file (entry tickets)
            csv_reader = csv.reader(input_file)

            # write to the output file
            with open(self.file.get_output_file_path(),
                      mode='w', newline='', encoding="utf-8") as output_file:
                csv_writer = csv.writer(output_file)
                for row in csv_reader:
                    # if self.ticket:
                    # TODO: implement
                    row.append("Hello world")
                    csv_writer.writerow(row)
