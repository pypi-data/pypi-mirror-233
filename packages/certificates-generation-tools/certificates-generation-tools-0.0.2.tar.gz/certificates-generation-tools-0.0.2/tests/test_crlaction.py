import unittest
import datetime
from logging import getLogger
from freezegun import freeze_time
from pydantic import ValidationError

from certificates_generation_tools.actions.crl import CrlAction


class TestCrlAction(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "crl_action"}
        # "Checking sign_keyid error message for crlaction")
        options = {
            **base_options,
        }
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking offsetValidityTime error message for crlaction")
        options = {**base_options, "sign_keyid": "key", "offsetValidityTime": "toto"}
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking offsetExpirationTime error message for crlaction")
        options = {**base_options, "sign_keyid": "key", "offsetExpirationTime": "toto"}
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking validityTime error message for crlaction")
        options = {**base_options, "sign_keyid": "key", "validityTime": "toto"}
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking expirationTime error message for crlaction")
        options = {**base_options, "sign_keyid": "key", "expirationTime": "toto"}
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking cert_id error message for revoked certificate in crlaction"
        options = {
            **base_options,
            "sign_keyid": "key",
            "revokedCerts": [{"revocationDate": "2020-07-06"}],
        }
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking revocationDate error message for revoked certificate in crlaction"
        options = {
            **base_options,
            "sign_keyid": "key",
            "revokedCerts": [{"cert_id": "key", "revocationDate": "toto"}],
        }
        with self.assertRaises(ValidationError):
            CrlAction("crl_action", options, None)
        # "Checking success crlaction check_options with validityTime, expirationTime, offsetValidityTime and offsetExpirationTime dates"
        options = {
            **base_options,
            "sign_keyid": "key",
            "ca_id": "ca",
            "validityTime": "2019-05-12",
            "expirationTime": "2018-05-12",
            "offsetValidityTime": 10,
            "offsetExpirationTime": 30,
        }
        CrlAction("crl_action", options, None)
        # "Checking success crlaction check_options with no dates")
        options = {**base_options, "sign_keyid": "key", "ca_id": "ca"}
        CrlAction("crl_action", options, None)
        # "Checking success for revoked certificate in crlaction")
        options = {
            **base_options,
            "sign_keyid": "key",
            "ca_id": "ca",
            "revokedCerts": [{"cert_id": "key", "revocationDate": "2020-07-06"}],
        }
        CrlAction("crl_action", options, None)

    @freeze_time("05-31-2014")
    def test__format_dates(self):
        """
        crl = CrlAction( 'crl_action', {})
        formatted_options = {}
        attempt_formatted_options = {
            'offsetValidityTime': 0,
            'offsetExpirationTime': 0,
            'expirationTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
            'validityTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
        }
        crl._format_dates(formatted_options, None)
        self.assertEqual(formatted_options, attempt_formatted_options, None)

        formatted_options = {'offsetValidityTime': 100}
        attempt_formatted_options = {
            'offsetValidityTime': 100,
            'offsetExpirationTime': 0,
            'expirationTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
            'validityTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
        }
        crl._format_dates(formatted_options, None)
        self.assertEqual(formatted_options, attempt_formatted_options, None)

        formatted_options = {'offsetExpirationTime': 100,
                             'offsetValidityTime': 100, 'expirationTime': '2016-05-30'}
        attempt_formatted_options = {
            'offsetExpirationTime': 100,
            'offsetValidityTime': 100,
            'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
            'validityTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
        }
        crl._format_dates(formatted_options, None)
        self.assertEqual(formatted_options, attempt_formatted_options, None)

        formatted_options = {'offsetExpirationTime': 100,
                             'offsetValidityTime': 200, 'validityTime': '2016-05-30'}
        attempt_formatted_options = {
            'offsetExpirationTime': 100,
            'offsetValidityTime': 200,
            'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
            'validityTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 200000),
        }
        crl._format_dates(formatted_options, None)
        self.assertEqual(formatted_options, attempt_formatted_options, None)

        formatted_options = {'validityTime': '2016-05-31',
                             'expirationTime': '2016-05-30'}
        attempt_formatted_options = {
            'offsetExpirationTime': 0,
            'offsetValidityTime': 0,
            'validityTime': datetime.datetime(2016, 5, 31, 0, 0, 0, 0),
            'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 0)
        }
        crl._format_dates(formatted_options, None)
        self.assertEqual(formatted_options, attempt_formatted_options, None)
        """
