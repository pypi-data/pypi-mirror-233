"""
cli module
"""
import click
from lottostar.app.file_processor.file_locator import FileLocator
from lottostar.app.file_processor.csv_processor import WinningEntryCsvProcessor, \
    OutputCsvProcessor
from lottostar.app.ballsets.main import BallSet
from lottostar.app.tickets.main import Ticket



@click.group()
def cli():
    """
    cli group
    """
    pass  # pylint: disable=unnecessary-pass

@click.command()
@click.option("-f", "--filename",
                prompt="Please enter the lottery results filename",
                required=True)
def process_lottery_results(filename: str) -> None:
    """
    Process an independent national lottery results.
    lottery_results_filename: the filename of the lottery results
    """
    file_locator = FileLocator(filename)
    winning_entry_numbers = WinningEntryCsvProcessor(file_locator)\
        .process()
    ballset = BallSet(winning_entry_numbers)
    winning_ticket = Ticket(ballset)

    OutputCsvProcessor(file_locator, winning_ticket).process()
    # print(ballset.additional_ballsets)
    # print(lottery_results_file.get_results_file_path())
    # print(lottery_results_file.get_output_file_path())
    # print(lottery_results_file.get_entry_tickets_file_path())

def process_all_lottery_results() -> None:
    """
    process all 30 independent national lottery results
    """
    pass  # pylint: disable=unnecessary-pass


cli.add_command(process_lottery_results, "process")  # command name
