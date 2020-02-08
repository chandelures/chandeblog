(function () {
    "use strict";

    $.extend(blog.handler, {
        //初始化目录
        initToc: function ($toc) {
            var
                offset = 75;
            $toc
                .find("ul")
                .addClass("ui link list")
            ;
            $toc
                .find("a")
                .addClass("item")
            ;
            $toc
                .find("a")
                .on("click", function (e) {
                    e = e || window.event;
                    e.preventDefault();
                    var target = $(this).prop('hash');
                    $('html,body').animate({scrollTop: $(target).offset().top - offset + 1})
                })
            ;
        },

        //实现滚动目录
        scollToc: function ($content, offset=75) {
            var
                $h = $content.find("h2, h3");

            var
                $activeH2 = $h.first(),
                $activeH3 = $activeH2;

            $h
                .visibility({
                    offset: offset,
                    once: false,
                    observeChanges: false,
                    onTopPassed: function () {
                        if (this.tagName === 'H2') {
                            $activeH2.removeClass('active');
                            $activeH3.removeClass('active');
                            $activeH2 = $("[href='#" + $(this).attr("id") + "']").addClass("active");
                        } else if (this.tagName === 'H3') {
                            $activeH3.removeClass('active');
                            $activeH3 = $("[href='#" + $(this).attr("id") + "']").addClass("active");
                        }
                    },
                    onBottomPassedReverse: function () {
                        $activeH2.removeClass('active');
                        $activeH3.removeClass('active');
                        $activeH2 = $("[href='#" + $(this).attr("id") + "']").addClass("active");
                    },
                })
            ;
        },

        //初始化CKEditor
        initTextarea: function ($textarea) {
            let comment_editor = CKEDITOR.replace($textarea.attr("id"), {
                customConfig: '/static/blog/js/ckeditor_config.js'
            });
            comment_editor.on('required', function (evt) {
                comment_editor.showNotification('请填写此字段', 'warning');
                evt.cancel();
            });
        },

        //初始化评论模态框
        initCommentModal: function ($button, $modal) {
            $button.on("click", function () {
                $modal
                    .modal({
                        onShow: function () {
                            var
                                postId = $button.data('postid'),
                                replyUsername = $button.data('replyusername'),
                                parentCommentId = $button.data('parentcommentid'),
                                modalTitleText = '回复给 ' + replyUsername,
                                action = "/comment/post-comment/" + postId + "/" + parentCommentId,
                                modal = $(this);

                            modal
                                .find("form")
                                .attr("action", action);

                            modal
                                .find('.header')
                                .text(modalTitleText);

                            if (modal.find(".cke").length === 0)
                                blog.handler.initTextarea(modal.find("textarea"));
                        },
                    })
                    .modal('show');
            });
        }
    });

    blog.before = {
        base: function () {
            blog.handler.initHighlighting();
        }
    };

    blog.ready.post = function () {
        var
            $toc = $(".toc"),
            $sticky = $(".ui.sticky"),
            $postContent = $("#postContent"),
            $commentBodyTextarea = $("#comment_body"),
            $commentReply = $(".reply"),
            $commentModal = $(".ui.modal.comment-modal"),
            $toUpButton = $("#toUp");

        var
            offset = 75;

        blog.handler.toUp($toUpButton);

        blog.handler.initToc($toc);

        blog.handler.scollToc($postContent, 75);

        $sticky
            .sticky({
                silent: true,
                offset: offset,
                context: '#post'
            })
        ;

        blog.handler.initTextarea($commentBodyTextarea);

        $commentReply
            .each(function () {
                blog.handler.initCommentModal($(this), $commentModal);
            })
        ;
    };

    blog.bootstrap();
})();