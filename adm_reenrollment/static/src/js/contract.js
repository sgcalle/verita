odoo.define('adm.reenrollment.form.contract', require => {
    "use strict";

    require('adm.reenrollment.form');

    function onReady() {
        console.log("Testing!");
    }

    /*
        I know I can use $(document).ready...
        I will use for others, I just use this for learning purposes :P so
        Let's learn together
     */
    if (document.readyState !== 'loading') {
        onReady();
    } else {
        document.addEventListener('DOMContentLoaded', onReady);
    }
})