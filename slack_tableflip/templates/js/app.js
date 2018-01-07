'use strict';

jQuery(document).ready(function ($) {

    if (window.location.search !== '') {
        // Remove everything after '?'
        var clean_url = window.location.href.split('?')[0];

        // Update URL
        window.history.replaceState(null, null, clean_url);
    }

    $('.close').on('click', function(e) {
        e.preventDefault();

        // Get notice element
        var $el = $('.alert');

        // Remove notice
        $el.fadeTo(100, 0, function () {
            $el.slideUp(100, function () {
                $el.remove();
            });
        });
    });
});
