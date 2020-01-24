(function () {
    "use strict";

    var ready = function () {
        var
            $tocContainer = $(".post-detail .overlay"),
            $toc = $(".toc"),
            $postDetail = $("#postDetail"),
            $toUpButton = $("#toUp");

        blog.handler.toUp($toUpButton);

        blog.handler.initToc($toc, $postDetail);

        $tocContainer
            .visibility({
                type: 'fixed',
                offset: 75
            })
        ;

        blog.handler.initHighlighting();
    };


    $(function () {
        ready();
    });
})();