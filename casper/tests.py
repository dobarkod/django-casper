from django.test import LiveServerTestCase
from subprocess import Popen, PIPE
import os.path
import sys

__all__ = ['CasperTestCase']


class CasperTestCase(LiveServerTestCase):
    """LiveServerTestCase subclass that can invoke CasperJS tests."""

    def casper(self, test_filename, **kwargs):
        """CasperJS test invoker.

        Takes a test filename (.js) and optional arguments to pass to the
        casper test.

        Returns True if the test(s) passed, and False if any test failed.

        Since CasperJS startup/shutdown is quite slow, it is recommended
        to bundle all the tests from a test case in a single casper file
        and invoke it only once.
        """

        kwargs.update({
            'load-images': 'no',
            'disk-cache': 'no',
            'ignore-ssl-errors': 'yes',
            'url-base': self.live_server_url
        })
        cmd = ['casperjs', 'test', '--no-colors']
        cmd.extend([('--%s=%s' % i) for i in kwargs.iteritems()])
        cmd.append(test_filename)

        p = Popen(cmd, stdout=PIPE, stderr=PIPE,
            cwd=os.path.dirname(test_filename))
        out, err = p.communicate()
        if p.returncode != 0:
            sys.stdout.write(out)
            sys.stderr.write(err)
        return p.returncode == 0
