import unittest
import datetime
from freezegun import freeze_time
from cryptography import x509
from logging import getLogger
from pydantic import ValidationError
from certificates_generation_tools.actions.cert import CertAction, format_extensions


class TestCertAction(unittest.TestCase):
    def setup(self):
        pass

    def test_check_options(self):
        base_options = {"kind": "", "name": "cert_action"}
        # "Checking private_keyid error message for certaction")
        options = {
            **base_options,
        }
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking autosign error message for certaction")
        options = {**base_options, "private_keyid": "key"}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking autosign error message for certaction")
        options = {**base_options, "private_keyid": "key", "autosign": False}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking offsetNotBefore error message for certaction")
        options = {**base_options, "private_keyid": "key", "offsetNotBefore": "toto"}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking offsetNotAfter error message for certaction")
        options = {"private_keyid": "key", "offsetNotAfter": "toto"}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking notBefore error message for certaction")
        options = {**base_options, "private_keyid": "key", "notBefore": "toto"}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking notAfter error message for certaction")
        options = {**base_options, "private_keyid": "key", "notAfter": "toto"}
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking alternativeNames error message for certaction")
        options = {
            **base_options,
            "private_keyid": "key",
            "autosign": True,
            "alternativeNames": "toto",
        }
        with self.assertRaises(ValidationError):
            CertAction("cert_action", options, None)
        # "Checking success certaction check_options with notBefore/After and offsetNotBefore/After dates, with autosign"
        options = {
            **base_options,
            "private_keyid": "key",
            "notAfter": "2019-05-12",
            "notBefore": "2018-05-12",
            "offsetNotAfter": 10,
            "offsetNotBefore": 30,
            "autosign": True,
        }
        CertAction("cert_action", options, None)
        # "Checking success certaction check_options with autosign False and no dates"
        options = {
            **base_options,
            "private_keyid": "key",
            "autosign": False,
            "sign_keyid": "titi",
        }
        CertAction("cert_action", options, None)
        # "Checking success certaction with no dates and no autosign defined"
        options = {**base_options, "private_keyid": "key", "sign_keyid": "titi"}
        CertAction("cert_action", options, None)

    @freeze_time("05-31-2014")
    def test__format_dates(self):
        """
            cert = CertAction( 'cert_action')
            formatted_options = {}
            attempt_formatted_options = {
                'offsetNotBefore': 0,
                'offsetNotAfter': 0,
                'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
                'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 0)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            formatted_options = {'offsetNotBefore': 100}
            attempt_formatted_options = {
                'offsetNotBefore': 100,
                'offsetNotAfter': 0,
                'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 0)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            formatted_options = {'offsetNotBefore': 100, 'offsetNotAfter': 100}
            attempt_formatted_options = {
                'offsetNotBefore': 100,
                'offsetNotAfter': 100,
                'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            formatted_options = {'offsetNotBefore': 100,
                                'offsetNotAfter': 100, 'notAfter': '2016-05-30'}
            attempt_formatted_options = {
                'offsetNotBefore': 100,
                'offsetNotAfter': 100,
                'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            formatted_options = {'offsetNotBefore': 100,
                                'offsetNotAfter': 200, 'notBefore': '2016-05-30'}
            attempt_formatted_options = {
                'offsetNotBefore': 100,
                'offsetNotAfter': 200,
                'notBefore': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
                'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 200000)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            formatted_options = {
                'notBefore': '2016-05-31', 'notAfter': '2016-05-30'}
            attempt_formatted_options = {
                'offsetNotBefore': 0,
                'offsetNotAfter': 0,
                'notBefore': datetime.datetime(2016, 5, 31, 0, 0, 0, 0),
                'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 0)
            }
            cert._format_dates(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

        def test_format_extensions(self):
            cert = CertAction( 'cert_action')
            formatted_options = {}
            attempt_formatted_options = {'extensions': []}
            format_extensions(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            cert = CertAction( 'cert_action')
            formatted_options = {'isCa': False}
            attempt_formatted_options = {'isCa': False, 'extensions': []}
            format_extensions(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)

            cert = CertAction( 'cert_action')
            formatted_options = {'isCa': True}
            attempt_formatted_options = {'isCa': True, 'extensions': [
                x509.Extension(
                    x509.OID_BASIC_CONSTRAINTS,
                    critical=True,
                    value=x509.BasicConstraints(ca=True, path_length=None)
                )
            ]}
            format_extensions(formatted_options, None)
            self.assertEqual(formatted_options,attempt_formatted_options, None)
        """
