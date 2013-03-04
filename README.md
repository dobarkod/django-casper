# Django Casper test integration

[![Build Status](https://travis-ci.org/dobarkod/django-casper.png?branch=master)](https://travis-ci.org/dobarkod/django-casper)

A Django application that makes it easy to use CasperJS/PhantomJS for
automated live testing of JavaScript and front/back integration for your
web applications.

[PhantomJS](http://phantomjs.org/) is a headless WebKit with JavaScript
API. It has fast and native support for various web standards.

[CasperJS](http://casperjs.org/) is a navigation scripting & testing utility
for PhantomJS, written in Javascript. While PhantomJS provides bare
essentials, CasperJS provides a simple testing framework specially optimized
for Phantom.

CasperJS assumes there is a web server to connect to while doing the tests.
While it can be done with a bit of creative shell scripting, it's not
immediately obvious how to use CasperJS in context of Django tests, ie.
for its [LiveServerTestCase](https://docs.djangoproject.com/en/dev/topics/testing/overview/#django.test.LiveServerTestCase)
tests.

This is where Django Casper comes in.

## How it works

`casper.CasperTestCase` subclasses `LiveServerTestCase` and adds a `casper`
method that can run a CasperJS test case (it is recommended to run multiple
tests in one run to minimize PhantomJS startup / shutdown time (it is quite
slow), but not neccessary) and return whether the test was successful.

The rest of the usage is a usual. Set up the database/fixtures, run the
test(s), assert that everything works as expected.

## Installation and requirements

Django Casper requires a working PhantomJS and CasperJS install, ie. the
`casperjs` command should be available. Refer to the CasperJS page on the
installation details for your system.

Other than that, Django Casper has no additional requirements (it's useless
without a Django project, though).

Download and installation procedure:

    # Download from GitHub
    git clone git@github.com:dobarkod/django-casper.git
    cd django-casper

    # Build
    python setup.py build

    # Optionally, run the self-test
    python setup.py

    # Install it
    python setup.py install

## Usage

First, add `casper` to your `INSTALLED_APPS`.

Then, create the Python part of your tests:

    from casper.tests import CasperTestCase
    import os.path

    class MyTest(CasperTestCase):
        def test_something(self):
            self.assertTrue(self.casper(
                os.path.join(os.path.dirname(__file__),
                    'casper-tests/test.js')))

Then, create the CasperJS part. Create a `casper-tests` directory somewhere
(eg. in your `tests` directory). Copy `djangocasper.js` helper JS module
from `/wherever/you/installed/django-casper/casper/jslib/` to this directory.
Then, create your CasperJS tests in it.

For example, this test asserts that there's a Login button on the home
page (relative URL `/`), and clicking it sends you to the login page
(relative URL `/login/`):

    casper.test.comment('Casper+Django integration example');
    var helper = require('./djangocasper.js');
    helper.scenario('/',
        function() {
            this.test.assertSelectorHasText('input[type="button"]', 'Login',
                "The home page has a Login button");
            this.click('input[type="button"]');
        },
        function() {
            helper.assertAbsUrl('/login/',
                "After clicking Login, we're redirected to login page");
        }
    );

For more examples, have a look at the django-casper test suite, the source
for the `djangocasper.js` helper and
[CasperJS Tester API](http://casperjs.org/api.html#tester).

## Passing extra arguments

Sometimes you need to pass extra arguments to your JS tests, for example,
username and password to log in with, or and ID of some object to manipulate.

You can do so by passing them as keyword arguments to the `casper` method
in your Python tests:

    def test_user_can_log_in(self):
        ...  # create user in the database
        self.assertTrue(self.casper(
            os.path.join(os.path.dirname(__file__),
                'casper-tests/test.js')),
            user=fixture_username,
            pass=fixture_password)

Then access these keyword arguments from the JS file:

    helper.scenario('/login/',
        function() {
            this.fill('form[method=post]', {
                username: casper.cli.options['user'],
                password: casper.cli.options['pass']
            }, true);
        }
    );

## Caveats

Phantom/Casper testing is *very slow* compared to Django's
[TestClient](https://docs.djangoproject.com/en/dev/intro/tutorial05/#the-django-test-client).
Whenever you have a page that can be accurately tested using only TestClient,
use it, and use Phantom/Casper only for tests where you need to test the
JavaScript behaviour.

Phantom hammers the Django's built-in live testserver a lot, as it requests
all the referenced static assets as well as the page itself, and this can
sometimes result in a deadlock. To avoid this, the runner is limited to 60
seconds per JS file (see the source of `djangocasper.js` for details).

Prior to Django 1.5, Django incorrectly reported last-modified time for
static files, which results in Phantom re-requesting every static file
always, even if it already has uptodate version. This was fixed in Django 1.5,
so it is recommended to use 1.5 or higher version of Django.

## Static files caching

A further speed optimization is possible if you're willing to monkeypatch
Django's test staticfiles handler to tell Phantom to unconditionally cache
the file for a while (by setting the `Expires` HTTP header). If you do so,
you should take care to clear Phantom's disk-cache before the tests start,
so it only caches things between cases of the same test run and doesn't get
stale.

To do so, set `use_phantom_disk_cache` class variable in your test case class:

    class MyTest(CasperTestCase):
        use_phantom_disk_cache = True
        ...

To clean the PhantomJS disk cache, remove `~/.qws/cache/Ofi\ Labs/PhantomJS/`
(as this is pretty-much undocumented feature, make sure to check what the
cache folder of *your* PhantomJS installation is, as it can vary depending
on the underlying OS and the PhantomJS version).

## License

Copyright (C) 2013. by Django Casper contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
