module.exports = (function() {
    var first_scenario = true;

    function scenario() {
        var base_url = casper.cli.options['url-base'];
        var start_url = base_url + arguments[0];
        var i;

        if (first_scenario) {
            casper.options.timeout = 60000;
            casper.options.onTimeout = function() {
                casper.die("Timed out after 60 seconds.", 1);
            };

            casper.start(start_url, arguments[1]);
            first_scenario = false;
        } else {
            casper.thenOpen(start_url, arguments[1]);
        }

        for (i = 2; i < arguments.length; i++) {
            casper.then(arguments[i]);
        }
    }

    function run() {
        casper.run(function() { this.test.done(); });
    }

    function assertAbsUrl(rel_url, str_msg) {
        var regex_str = '^' + casper.cli.options['url-base'] + rel_url.replace(/\?/g, '\\?') + '$';
        casper.test.assertUrlMatch(new RegExp(regex_str), str_msg);
    }

    function qunit (url) {
        scenario(url, function() {
            casper.waitFor(function() {
                return casper.evaluate(function() {
                    var el = document.getElementById('qunit-testresult');
                    return el && el.innerText.match('completed');
                });
            }, function() {
                casper.echo("Test output: " + casper.evaluate(function(){
                    return document.getElementById('qunit-testresult').innerText;
                }), 'INFO');
                casper.test.assertEquals(
                    casper.evaluate(function(){
                        return document.getElementById('qunit-testresult')
                            .getElementsByClassName('failed')[0].innerText;
                    }), "0");
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
