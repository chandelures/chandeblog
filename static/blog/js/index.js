(function () {
    "use strict";

    var ready = function () {
        var
            $toUpButton = $("#toUp"),
            $loadPostListButton = $("#loadPostListButton");

        blog.handler.loadPostList($loadPostListButton, 5);

        blog.handler.toUp($toUpButton);

        blog.handler.initHighlighting();
    };

    hljs.initHighlightingOnLoad();

    $(function () {
        ready();
    });
})();