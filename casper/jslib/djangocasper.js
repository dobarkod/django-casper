/* global casper: true, phantom: true */

module.exports = (function() {
    var firstScenario = true;

    function opt(name, dfl) {
        if (casper.cli.options.hasOwnProperty(name)) {
            return casper.cli.options[name];
        } else {
            return dfl;
        }
    }

    function injectCookies() {
        var m = opt('url-base').match(/https?:\/\/([^:]+)(:\d+)?\//);
        var domain = m ? m[1] : 'localhost';

        for (var key in casper.cli.options) {
            if (key.indexOf('cookie-') === 0) {
                var cn = key.substring('cookie-'.length);
                var c = phantom.addCookie({
                    name: cn,
                    value: opt(key),
                    domain: domain
                });
            }
        }
    }

    function scenario() {
        var baseUrl = opt('url-base');
        var startUrl = baseUrl + arguments[0];
        var i;

        casper.options.viewportSize = {
            width: 1024,
            height: 768
        };

        if (firstScenario) {
            injectCookies();

            casper.options.timeout = 60000;
            casper.options.onTimeout = function() {
                casper.die('Timed out after 60 seconds.', 1);
            };

            casper.start(startUrl, arguments[1]);
            firstScenario = false;
        } else {
            casper.thenOpen(startUrl, arguments[1]);
        }

        for (i = 2; i < arguments.length; i++) {
            casper.then(arguments[i]);
        }
    }

    function run() {
        casper.run(function() { this.test.done(); });
    }

    function assertAbsUrl(relUrl, strMsg) {
        var regexStr = '^' + casper.cli.options['url-base'] +
            relUrl.replace(/\?/g, '\\?') + '$';
        casper.test.assertUrlMatch(new RegExp(regexStr), strMsg);
    }

    function qunit(url) {
        scenario(url, function() {
            casper.waitFor(function() {
                return casper.evaluate(function() {
                    var el = document.getElementById('qunit-testresult');
                    return el && el.innerText.match('completed');
                });
            }, function() {
                casper.echo('Test output: ' + casper.evaluate(function() {
                    return document.getElementById('qunit-testresult')
                        .innerText;
                }), 'INFO');
                casper.test.assertEquals(
                    casper.evaluate(function() {
                        return document.getElementById('qunit-testresult')
                            .getElementsByClassName('failed')[0].innerText;
                    }), '0');
            });
        });
    }

    return {
        scenario: scenario,
        run: run,
        assertAbsUrl: assertAbsUrl,
        qunit: qunit
    };
})();
