import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import mock_open, patch

from monaco_2018_racing.report import (
    Race, Racer, SortedRaceResults, build_report,
    format_timedelta, parse_abbreviations,
    parse_log, sort_race_results
)

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

DATE_FORMAT = "%Y-%m-%d_%H:%M:%S.%f"


class TestReportFunctions(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="ABC2018-05-24_12:00:00.000\nXYZ2018-05-24_12:01:01.123"
    )
    def test_parse_log(self, mock_file):
        expected_result = {
            "ABC": datetime.strptime("2018-05-24_12:00:00.000", DATE_FORMAT),
            "XYZ": datetime.strptime("2018-05-24_12:01:01.123", DATE_FORMAT)
        }
        self.assertEqual(parse_log("fake_path.log"), expected_result)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="LHM_Lewis Hamilton_MERCEDES\nSVF_Sebastian Vettel_FERRARI"
    )
    def test_parse_abbreviations(self, mock_file):
        expected_result = {
            "LHM": Racer("Lewis Hamilton", "MERCEDES"),
            "SVF": Racer("Sebastian Vettel", "FERRARI")
        }
        self.assertEqual(parse_abbreviations("fake_path.txt"), expected_result)

    @patch("web_report_monaco_2018_racing.report.parse_log")
    @patch("web_report_monaco_2018_racing.report.parse_abbreviations")
    def test_build_report(self, mock_parse_abbreviations, mock_parse_log):
        mock_parse_log.side_effect = [
            {"LHM": datetime(2018, 5, 24, 12, 0, 0),
             "SVF": datetime(2018, 5, 24, 12, 1, 1)},
            {"LHM": datetime(2018, 5, 24, 12, 1, 0),
             "SVF": datetime(2018, 5, 24, 12, 2, 1)}
        ]
        mock_parse_abbreviations.return_value = {
            "LHM": Racer("Lewis Hamilton", "MERCEDES"),
            "SVF": Racer("Sebastian Vettel", "FERRARI")
        }

        expected_result = {
            "LHM": Race(
                Racer("Lewis Hamilton", "MERCEDES"),
                datetime(2018, 5, 24, 12, 0, 0),
                datetime(2018, 5, 24, 12, 1, 0)
            ),
            "SVF": Race(
                Racer("Sebastian Vettel", "FERRARI"),
                datetime(2018, 5, 24, 12, 1, 1),
                datetime(2018, 5, 24, 12, 2, 1)
            )
        }

        self.assertEqual(build_report(
            "start.log", "end.log", "abbr.txt"), expected_result)

    def test_format_timedelta(self):
        self.assertEqual(format_timedelta(
            timedelta(minutes=1, seconds=2, milliseconds=123)), "1:02.123")

    def test_sort_race_results(self):
        race_results = {
            "LHM": Race(
                Racer("Lewis Hamilton", "MERCEDES"),
                datetime(2018, 5, 24, 12, 0, 0),
                datetime(2018, 5, 24, 12, 1, 0)
            ),
            "SVF": Race(
                Racer("Sebastian Vettel", "FERRARI"),
                datetime(2018, 5, 24, 12, 1, 1),
                datetime(2018, 5, 24, 12, 2, 1)
            )
        }
        sorted_results = sort_race_results(race_results, order="asc")

        expected = SortedRaceResults(
            positive_times=[
                ("LHM", race_results["LHM"]),
                ("SVF", race_results["SVF"])
            ],
            negative_times=[]
        )

        self.assertEqual(sorted_results.positive_times,
                         expected.positive_times)
        self.assertEqual(sorted_results.negative_times,
                         expected.negative_times)
