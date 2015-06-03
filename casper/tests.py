from django.test import LiveServerTestCase
from subprocess import Popen, PIPE
import os
import sys

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.staticfiles.views import serve
from django.utils.http import http_date
from django.conf import settings

__all__ = ['CasperTestCase']


def staticfiles_handler_serve(self, request):
    import time
    resp = serve(request, self.file_path(request.path), insecure=True)
    if resp.status_code == 200:
        resp["Expires"] = http_date(time.time() + 24 * 3600)
    return resp


class CasperTestCase(LiveServerTestCase):
    """LiveServerTestCase subclass that can invoke CasperJS tests."""

    use_phantom_disk_cache = False
    load_images = False
    no_colors = True

    def __init__(self, *args, **kwargs):
        super(CasperTestCase, self).__init__(*args, **kwargs)
        if self.use_phantom_disk_cache:
            StaticFilesHandler.serve = staticfiles_handler_serve

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
            'load-images': 'yes' if self.load_images else 'no',
            'disk-cache': 'yes' if self.use_phantom_disk_cache else 'no',
            'ignore-ssl-errors': 'yes',
            'url-base': self.live_server_url,
            'log-level': 'debug' if settings.DEBUG else 'error',
        })

        cn = settings.SESSION_COOKIE_NAME
        if cn in self.client.cookies:
            kwargs['cookie-' + cn] = self.client.cookies[cn].value

        cmd = ['casperjs', 'test']

        if self.no_colors:
            cmd.append('--no-colors')

        if settings.DEBUG:
            cmd.append('--verbose')

        cmd.extend([('--%s=%s' % i) for i in kwargs.iteritems()])
        cmd.append(test_filename)

        node_env = os.environ.copy()
        node_env['PATH'] = \
            os.path.join(os.getcwd(), 'node_modules/.bin') + \
            ":" + node_env['PATH']
        p = Popen(cmd, env=node_env, stdout=PIPE, stderr=PIPE,
            cwd=os.path.dirname(test_filename))  # flake8: noqa
        out, err = p.communicate()
        if p.returncode != 0:
            sys.stdout.write(out)
            sys.stderr.write(err)
        return p.returncode == 0
