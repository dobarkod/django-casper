casper.test.comment('Casper+Django integration example');

/* You will probably want to copy the helper module to your js tests dir. */
var helper = require('../../../casper/jslib/djangocasper.js');

helper.scenario('/',
    function() {
        this.test.assertSelectorHasText('em', 'django-casper',
            "There's a mention of django-casper on the page");
        this.click('a');
    },
    function() {
        this.test.assertSelectorHasText('#messages p', 'Good times!',
            "When the link is clicked, a message is added to the page");
    }
);

helper.run();