import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.key import KeyAction


class TestKeyAction(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "key_action"}
        # "Checking success keyaction without given bits size")
        options = {
            **base_options,
        }
        KeyAction("key_action", options, None)
        # "Checking success keyaction with bits size given")
        options = {**base_options, "bits": "4096"}
        KeyAction("key_action", options, None)
