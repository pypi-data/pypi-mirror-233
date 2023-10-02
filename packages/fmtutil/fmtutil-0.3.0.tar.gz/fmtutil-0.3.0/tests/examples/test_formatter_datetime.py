# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object examples for Datetime.
"""
import unittest
from datetime import datetime

import fmtutil.formatter as fmt


class DatetimeExampleTestCase(unittest.TestCase):
    def test_format_example(self):
        dt = fmt.Datetime.parse(
            "20230907 23:08:56.041000", "%Y%m%d %H:%M:%S.%f"
        )

        # Common format of Datetime use-case.
        self.assertEqual("2023", dt.format("%Y"))
        self.assertEqual("09", dt.format("%m"))
        self.assertEqual("9", dt.format("%-m"))
        self.assertEqual("07", dt.format("%d"))
        self.assertEqual("7", dt.format("%-d"))
        self.assertEqual("23", dt.format("%H"))
        self.assertEqual("23", dt.format("%-H"))
        self.assertEqual("08", dt.format("%M"))
        self.assertEqual("8", dt.format("%-M"))
        self.assertEqual("56", dt.format("%S"))
        self.assertEqual("56", dt.format("%-S"))
        self.assertEqual("041000", dt.format("%f"))

    def test_format_example_special(self):
        dt = fmt.Datetime.parse(
            "20050904 19:08:56.041000", "%Y%m%d %H:%M:%S.%f"
        )

        self.assertEqual("05", dt.format("%y"))
        self.assertEqual("5", dt.format("%-y"))
        self.assertEqual("Sep", dt.format("%b"))
        self.assertEqual("September", dt.format("%B"))
        self.assertEqual("Sun", dt.format("%a"))
        self.assertEqual("Sunday", dt.format("%A"))
        self.assertEqual("0", dt.format("%w"))
        self.assertEqual("7", dt.format("%u"))
        self.assertEqual("07", dt.format("%I"))
        self.assertEqual("7", dt.format("%-I"))
        self.assertEqual("PM", dt.format("%p"))

    def test_format_example_numbers(self):
        dt = fmt.Datetime.parse(
            "20230205 01:25:36.141200", "%Y%m%d %H:%M:%S.%f"
        )

        self.assertEqual("036", dt.format("%j"))
        self.assertEqual("36", dt.format("%-j"))
        self.assertEqual("Sunday", dt.format("%A"))
        self.assertEqual("06", dt.format("%U"))  # Sunday
        self.assertEqual("05", dt.format("%W"))  # Monday

        dt = fmt.Datetime.parse(
            "20230910 03:12:07.000200", "%Y%m%d %H:%M:%S.%f"
        )

        self.assertEqual("253", dt.format("%j"))
        self.assertEqual("253", dt.format("%-j"))
        self.assertEqual("Sunday", dt.format("%A"))
        self.assertEqual("37", dt.format("%U"))  # Sunday
        self.assertEqual("36", dt.format("%W"))  # Monday

    def test_parse_examples(self):
        self.assertEqual(
            datetime(2021, 1, 1, microsecond=135000),
            fmt.Datetime.parse("2021-01-1 135043", "%Y-%m-%-d %f").value,
        )

        self.assertEqual(
            datetime(2023, 9, 5),
            fmt.Datetime.parse("2023-Sep Thursday 5", "%Y-%b %A %-d").value,
        )

        self.assertEqual(
            datetime(2023, 2, 5, 0, 0, 0),
            fmt.Datetime.parse("2023-Feb 05 36", "%Y-%b %W %-j").value,
        )

        self.assertEqual(
            datetime(2023, 9, 10, 0, 0, 0),
            fmt.Datetime.parse("2023-Sep 37 253", "%Y-%b %U %-j").value,
        )

        self.assertEqual(
            datetime(2023, 9, 10, 0, 0, 0),
            fmt.Datetime.parse("2023 37 253", "%Y %U %-j").value,
        )

        self.assertEqual(
            datetime(2023, 3, 1, 8, 0, 0),
            fmt.Datetime.parse("2023 D60, 08:00:00", "%Y D%-j, %I:%M:%S").value,
        )

        self.assertEqual(
            datetime(2023, 3, 1, 20, 0, 0),
            fmt.Datetime.parse(
                "2023 D60, 08:00:00PM", "%Y D%-j, %I:%M:%S%p"
            ).value,
        )
