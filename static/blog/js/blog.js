(function () {
    "use strict";

    $.extend(blog.handler, {
        //将指定标签变为激活状态
        activeAnchor: function ($header) {
            var id = $header.attr("id");
            return $("[href='#" + id + "']").addClass("active");
        },

        //初始化目录
        initToc: function ($toc) {
            var
                offset = 60;
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
                    $('html,body').scrollTop($(target).offset().top - offset + 2);
                })
            ;
        },

        //实现滚动目录
        scollToc: function ($content) {
            var
                $window = $(window),
                $h = $content.find("h2,h3"),
                offset = 60,
                activeH2 = $("body"),
                activeH3 = activeH2;
            $(window)
                .scroll(function () {
                    $h.each(function () {
                            var $this = $(this),
                                offsetTop = $this.offset().top - offset;
                            if ($window.scrollTop() > offsetTop) {
                                if (this.tagName === "H2") {
                                    activeH2.removeClass("active");
                                    activeH3.removeClass("active");
                                    activeH2 = blog.handler.activeAnchor($this);
                                    return true;

                                } else if (this.tagName === "H3") {
                                    activeH3.removeClass("active");
                                    activeH3 = blog.handler.activeAnchor($this);
                                    return true;
                                }
                            }
                        }
                    );
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

                            // modal.removeAttr('tabindex');
                            modal.find("form").attr("action", action);
                            modal.find('.header').text(modalTitleText);
                            if (modal.find(".cke").length === 0)
                                blog.handler.initTextarea(modal.find("textarea"));
                        },
                    })
                    .modal('show');
            });
        }
    });

    blog.ready.post = function () {
        var
            $toc = $(".toc"),
            $sticky = $(".ui.sticky"),
            $postDetail = $("#postDetail"),
            $commentBodyTextarea = $("#comment_body"),
            $commentReply = $(".reply"),
            $commentModal = $(".ui.modal"),
            $toUpButton = $("#toUp");

        blog.handler.toUp($toUpButton);

        blog.handler.initToc($toc);

        if (!(blog.handler.isIE())) blog.handler.scollToc($postDetail);

        $sticky
            .sticky({
                context: '#postDetail'
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