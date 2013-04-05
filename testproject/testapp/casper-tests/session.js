casper.test.comment('Casper+Django integration example');

/* You will probably want to copy the helper module to your js tests dir. */
var helper = require('../../../casper/jslib/djangocasper.js');

helper.scenario('/',
    function() {
        this.test.assertSelectorHasText('p.authorized', 'Hi there!',
            "The test client has successfully authorized");
    }
);

helper.run();