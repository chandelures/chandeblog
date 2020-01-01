(function () {
    "use strict";

    hljs.initHighlightingOnLoad(); //初始化代码块

    function initToc() {
        //初始化文章目录
        let navSelector = "#toc",
            toc = $(navSelector),
            body = $("body"),
            postCommentDivider = $("#post-comment-divider"),
            sidebar = $("#sidebar"),
            fadeInTime = 300,
            fadeOutTime = 300;

        Toc.init(toc);
        body.scrollspy({
            target: navSelector
        });

        $(window).scroll(function () {
            //侧边栏滚动监听
            if ($(this).scrollTop() > postCommentDivider.offset().top) {
                sidebar.fadeOut(fadeOutTime);
            } else {
                sidebar.fadeIn(fadeInTime);
            }
        }).scroll();
    }

    function initCommentForm() {
        //初始化评论表单
        let replaceTextarea = function (textareaId) {
            //替换文本框为富文本编辑器
            if ($("#" + textareaId).length > 0) {
                let comment_editor = CKEDITOR.replace(textareaId);
                comment_editor.on('required', function (evt) {
                    alert('请填写评论');
                    evt.cancel();
                });
            }
        };
        replaceTextarea('modal_comment_body');
        replaceTextarea('comment_body');

        let commentModal = $('#commentModal');
        commentModal.on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget),
                postId = button.data('postid'),
                replyUsername = button.data('replyusername'),
                parentCommentId = button.data('parentcommentid'),
                modalTitleText = '回复 ' + replyUsername,
                action = "/comment/post-comment/" + postId + "/" + parentCommentId,
                modal = $(this);

            modal.removeAttr('tabindex');
            modal.find("form").attr("action", action);
            modal.find('.modal-title').text(modalTitleText);
        });
    }

    function hoverComment() {
        //处理鼠标悬停评论事件
        let commentList = $(".comment");
        commentList.each(function () {
            $(this).hover(function () {
                $(this).find(".comment-toolbar").removeClass("d-none")
            });
            $(this).mouseleave(function () {
                $(this).find(".comment-toolbar").addClass("d-none")
            })
        })
    }

    $(function () {
        initCommentForm();
        initToc();
        hoverComment();
    });
})();