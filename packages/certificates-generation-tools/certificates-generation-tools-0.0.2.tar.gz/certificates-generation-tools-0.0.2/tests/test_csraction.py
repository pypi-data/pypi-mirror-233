import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.csr import CsrAction


class TestCsrAction(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "csr_action"}
        # "Checking private_keyid error message for csraction")
        options = {
            **base_options,
        }
        with self.assertRaises(ValidationError):
            CsrAction("csr_action", options, None)
        # "Checking success of check option for csraction")
        options = {**base_options, "private_keyid": "key"}
        CsrAction("csr_action", options, None)
