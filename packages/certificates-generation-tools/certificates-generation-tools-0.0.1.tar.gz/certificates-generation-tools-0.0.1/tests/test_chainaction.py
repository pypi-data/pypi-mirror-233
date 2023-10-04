import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.chain import ChainAction


class TestChainAction(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "chain_action"}
        # "Checking fail chainaction check_options with no certs_id")
        options = {
            **base_options,
        }
        with self.assertRaises(ValidationError):
            ChainAction("chain_action", options, None)
        # "Checking success chainaction check_options with no dates and no autosign defined")
        options = {**base_options, "certs_id": ["key"]}
        ChainAction("chain_action", options, None)
