(function () {
    "use strict";

    var ready = function () {
        var
            $tocContainer = $(".post-detail .overlay"),
            $toc = $(".toc"),
            $postDetail = $("#postDetail"),
            $commentBodyTextarea = $("#comment_body"),
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

        blog.handler.initTextarea($commentBodyTextarea);
    };


    $(function () {
        ready();
    });
})();