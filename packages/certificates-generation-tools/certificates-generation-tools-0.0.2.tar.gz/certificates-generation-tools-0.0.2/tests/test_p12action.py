import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.p12 import P12Action


class TestP12Action(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "p12_action"}
        # "Checking fail p12action check_options private_keyid")
        options = {
            **base_options,
        }
        with self.assertRaises(ValidationError):
            P12Action("p12_action", options, None)
        # "Checking fail p12action check_options certs_id")
        options = {**base_options, "private_keyid": "key"}
        with self.assertRaises(ValidationError):
            P12Action("p12_action", options, None)
        # "Checking success p12action check_options")
        options = {**base_options, "private_keyid": "key", "certs_id": ["key"]}
        P12Action("p12_action", options, None)
