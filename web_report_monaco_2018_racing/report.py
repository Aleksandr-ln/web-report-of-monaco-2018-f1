"""
Module: Formula 1 Racing Report Generator
------------------------------------------

This module processes log files containing Formula 1 racing data for the
Monaco 2018 Grand Prix qualification stage. It calculates lap times for racers,
sorts them by performance, and generates a formatted report.

Configuration:
    The paths for the required log files are imported from `config.py`:
    - START_LOG: Path to the start log file.
    - END_LOG: Path to the end log file.
    - ABBREVIATIONS_FILE: Path to the abbreviations file.

Classes:
    Racer: A dataclass representing a racer with a name and team.
    Race: A dataclass representing a race session with a racer, start time,
          end time, and lap time calculation.
    SortedRaceResults: A dataclass storing sorted race results into
          positive and negative lap times.

Functions:
    parse_log(file_path: str) -> Dict[str, datetime]:
        Parses a log file into a dictionary with abbreviations as keys
        and timestamps as values.

    parse_abbreviations(file_path: str) -> Dict[str, Racer]:
        Parses the abbreviations file into a dictionary with racer
        abbreviations as keys and `Racer` objects as values.

    build_report(
        start_path: str,
        end_path: str,
        abbreviations_path: str
        ) -> Dict[str, Race]:
        Builds a report by combining racer data with their start and end times.

    format_timedelta(delta: timedelta) -> str:
        Formats a timedelta object into 'm:ss.mmm'.

    sort_race_results(
        race_results: Dict[str, Race],
        order: str
    ) -> SortedRaceResults:
        Sorts race results into positive lap times and negative/zero lap times.

    print_report(
        sorted_results: SortedRaceResults
    ) -> str:
        Generates a formatted report for the top 15 racers and the rest.

Example Usage:
    report_data = build_report(START_LOG, END_LOG, ABBREVIATIONS_FILE)
    sorted_results = sort_race_results(report_data)
    print(print_report(sorted_results))
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

DATE_FORMAT = "%Y-%m-%d_%H:%M:%S.%f"


@dataclass
class Racer:
    """
    Represents a Formula 1 racer.

    Attributes:
        name (str): The name of the racer.
        team (str): The name of the team the racer belongs to.
    """
    name: str
    team: str


@dataclass
class Race:
    """
    Represents a race session for a specific driver.

    Attributes:
        racer (Racer): The racer object containing name and team.
        start_time (datetime): The start time of the race.
        end_time (datetime): The end time of the race.
    """
    racer: Racer
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def lap_time(self) -> Optional[timedelta]:
        """
        Calculates the lap time if both start and end times are available.
        If either start or end time is missing, returns timedelta(0).

        Returns:
            timedelta: The lap time as a timedelta object.
        """
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return timedelta(0)


@dataclass
class SortedRaceResults:
    positive_times: List[Tuple[str, Race]]
    negative_times: List[Tuple[str, Race]]


def parse_log(file_path: str) -> Dict[str, datetime]:
    """
    Parses a log file into a dictionary where keys are abbreviations
    and values are timestamps.

    Args:
        file_path (str): The path to the log file.

    Returns:
        Dict[str, datetime]: A dictionary mapping racer abbreviations
        to their timestamps.
    """
    log_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) < 26:
                continue
            abbr, datetime_ = line[:3], line[3:]
            log_data[abbr] = datetime.strptime(datetime_, DATE_FORMAT)
    return log_data


def parse_abbreviations(file_path: str) -> Dict[str, Racer]:
    """
    Parses the abbreviations file into a dictionary with racer abbreviations
    as keys and `Racer` objects as values.

    Args:
        file_path (str): The path to the abbreviations file.

    Returns:
        Dict[str, Racer]: A dictionary mapping racer abbreviations to
        `Racer` objects.
    """
    abbreviations = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            key, name, team = line.strip().split('_', 2)
            abbreviations[key] = Racer(name=name, team=team)
    return abbreviations


def format_timedelta(delta: timedelta) -> str:
    """
    Formats a timedelta object into 'm:ss.mmm'.

    Args:
        delta (timedelta): The time difference to format.

    Returns:
        str: The formatted time difference as a string.
    """
    total_seconds = delta.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = round((total_seconds % 1) * 1000)
    return f"{minutes}:{seconds:02}.{milliseconds:03}"


def build_report(
        start_path: str,
        end_path: str,
        abbreviations_path: str
) -> Dict[str, Race]:
    """
    Builds a report by combining racer data with their start and end times.

    Args:
        start_path (str): The path to the start log file.
        end_path (str): The path to the end log file.
        abbreviations_path (str): The path to the abbreviations file.

    Returns:
        Dict[str, Race]: A dictionary mapping racer abbreviations
        to `Race` objects.
    """
    start_data = parse_log(start_path)
    end_data = parse_log(end_path)
    abbreviations = parse_abbreviations(abbreviations_path)

    race_results = {
        abbr: Race(
            racer=abbreviations[abbr],
            start_time=start_data[abbr],
            end_time=end_data[abbr]
        )
        for abbr in start_data if abbr in end_data
    }
    return race_results


def sort_race_results(
        race_results: Dict[str, "Race"],
        order: str = "asc"
) -> SortedRaceResults:
    """
    Sorts race results into positive lap times and negative/zero lap times.

    Args:
        race_results (Dict[str, Race]): A dictionary mapping racer abbreviations to `Race` objects.
        order (str): The sorting order ('asc' or 'desc').

    Returns:
        SortedRaceResults: An object containing sorted positive and negative lap times.
    """

    positive_times = [
        (abbr, race) for abbr, race in race_results.items() if race.lap_time.total_seconds() > 0
    ]

    negative_times = [
        (abbr, race) for abbr, race in race_results.items() if race.lap_time.total_seconds() <= 0
    ]

    sorted_positives = sorted(
        positive_times,
        key=lambda item: item[1].lap_time.total_seconds(),
        reverse=(order == "desc")
    )

    sorted_negatives = sorted(
        negative_times,
        key=lambda item: item[1].lap_time.total_seconds(),
        reverse=(order == "desc")
    )

    return SortedRaceResults(sorted_positives, sorted_negatives)


def print_report(
        sorted_results: SortedRaceResults
) -> str:
    """"
    Generates a formatted report for the top 15 racers and the rest.

    Args:
        sorted_results (SortedRaceResults): A dataclass containing sorted race results.

    Returns:
        str: Formatted race report as a string.
    """
    sorted_lap_times = sorted_results.positive_times + sorted_results.negative_times

    max_name_width = max(len(race.racer.name) for _, race in sorted_lap_times)
    max_team_width = max(len(race.racer.team) for _, race in sorted_lap_times)
    max_line_number = len(sorted_lap_times)
    number_width = len(str(max_line_number))

    report_lines = []

    for count, (abbr, race) in enumerate(sorted_lap_times[:15], 1):
        report_lines.append(
            f"{str(count).rjust(number_width)}. "
            f"{race.racer.name:<{max_name_width}} | "
            f"{race.racer.team:<{max_team_width}} | "
            f"{format_timedelta(race.lap_time)}"
        )

    report_lines.append("\n" + "-" * (number_width + 2 +
                        max_name_width + 3 + max_team_width + 3 + 9) + "\n")

    for count, (abbr, race) in enumerate(sorted_lap_times[15:], 16):
        report_lines.append(
            f"{str(count).rjust(number_width)}. "
            f"{race.racer.name:<{max_name_width}} | "
            f"{race.racer.team:<{max_team_width}} | "
            f"{format_timedelta(race.lap_time)}"
        )

    return "\n".join(report_lines)
