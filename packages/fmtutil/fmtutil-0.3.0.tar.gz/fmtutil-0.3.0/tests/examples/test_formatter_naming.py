# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object examples for Naming.
"""
import unittest

import fmtutil.formatter as fmt


class NamingExampleTestCase(unittest.TestCase):
    def test_parse_examples(self):
        self.assertListEqual(
            ["monkey", "d", "luffy"],
            fmt.Naming.parse("monkey-d-luffy", "%k").value,
        )

        self.assertListEqual(
            ["monkey", "d", "luffy"],
            fmt.Naming.parse("monkey-d-luffy MDL", "%k %A").value,
        )

        self.assertListEqual(
            ["data", "is", "new", "oil"],
            fmt.Naming.parse("data_is_new_oil dtsnwl", "%s %v").value,
        )

        self.assertListEqual(
            ["data", "engine", "framework"],
            fmt.Naming.parse(
                "data_engine_framework dataengineframework", "%s %f"
            ).value,
        )

        self.assertEqual(
            ["data", "engine"],
            fmt.Naming.parse("dataengine de", "%f %a").value,
        )

        self.assertEqual(
            ["data", "engine"],
            fmt.Naming.parse("dataengine de dataEngine", "%f %a %c").value,
        )
