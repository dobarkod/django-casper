from casper.tests import CasperTestCase
import os.path

from django.contrib.auth.models import User


class CasperTestTestCase(CasperTestCase):
    """
    Yo dawg, I heard you like tests, so I put tests in your tests
    so you can test while you test.
    """

    def test_that_casper_integration_works(self):
        self.assertTrue(self.casper(
            os.path.join(os.path.dirname(__file__),
                'casper-tests/test.js')))  # flake8: noqa

    def test_that_casper_integration_works_when_test_fails(self):
        self.assertFalse(self.casper(
            os.path.join(os.path.dirname(__file__),
                'casper-tests/failing-test.js')))  # flake8: noqa

    def test_that_casper_can_reuse_session_cookie(self):
        u = User.objects.create_user(username='foo', password='bar')
        self.client.login(username='foo', password='bar')
        self.assertTrue(self.casper(
            os.path.join(os.path.dirname(__file__),
                'casper-tests/session.js')))  # flake8: noqa
