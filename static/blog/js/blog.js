(function () {
    "use strict";

    var ready = function () {
        var
            $tocContainer = $(".post-detail .overlay"),
            $toc = $(".toc"),
            $postDetail = $("#postDetail"),
            $commentBodyTextarea = $("#comment_body"),
            $commentReply = $(".reply"),
            $commentModal = $(".ui.modal"),
            $commentModalTextarea = $("#modal_comment_body"),
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

        // blog.handler.initTextarea($commentModalTextarea);

        $commentReply
            .each(function () {
                blog.handler.initCommentModal($(this),$commentModal);
            })
        ;
    };

    hljs.initHighlightingOnLoad();

    $(function () {
        ready();
    });
})();