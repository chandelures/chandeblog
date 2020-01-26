(function () {
    "use strict";

    window.blog = {
        handler: {},
    };

    blog.handler = {
        //回到顶部功能
        toUp: function ($button) {
            var fadeInTime = 300,
                fadeOutTime = 300,
                scrollSpace = 300,
                animateTime = 500;
            $button.click(function () {
                $('html,body').animate({scrollTop: 0}, animateTime);
            });
            $(window)
                .scroll(function () {
                    if ($(this).scrollTop() > scrollSpace) {
                        $button.fadeIn(fadeInTime);
                    } else {
                        $button.fadeOut(fadeOutTime);
                    }
                })
                .scroll()
            ;

        },

        initHighlighting: function () {
            hljs.initHighlightingOnLoad();
        },

        //将指定标签变为激活状态
        activeAnchor: function ($header) {
            var id = $header.attr("id");
            $("[href='#" + id + "']").addClass("active");
        },

        //将指定标签变为非激活状态
        deactiveAnchor: function ($toc, level) {
            if (level === 1) {
                $toc.find("ul > li > a").removeClass("active");
            } else if (level === 2) {
                $toc.find("ul > li > ul > li > a").removeClass("active");
            }
        },

        //判断页面是否到达底部
        isArriveBottom: function () {
            var $window = $(window),
                $document = $(document),
                error = 2,
                condition = $window.scrollTop() + $window.height() - $document.height();
            return (condition < error && condition > -error);
        },

        //初始化目录
        initToc: function ($toc, $content) {
            var
                $h = $content.find("h2,h3"),
                $window = $(window),
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
            $window
                .scroll(function () {
                    $h.each(function () {
                            var $this = $(this);
                            if (this.tagName === "H2") {
                                if ($window.scrollTop() > $this.offset().top - offset) {
                                    blog.handler.deactiveAnchor($toc, 1);
                                    blog.handler.activeAnchor($this);
                                }
                            } else if (this.tagName === "H3") {
                                if ($window.scrollTop() > $this.offset().top - offset) {
                                    blog.handler.deactiveAnchor($toc, 2);
                                    blog.handler.activeAnchor($this);
                                }
                            }
                        }
                    );
                    if (blog.handler.isArriveBottom()) {
                        var last = $h[$h.length - 1];
                        if (last.tagName === "H2") {
                            blog.handler.deactiveAnchor($toc, 1);
                            blog.handler.activeAnchor($(last));
                        } else if (last.tagName === "H3") {
                            blog.handler.deactiveAnchor($toc, 2);
                            blog.handler.activeAnchor($(last));
                        }
                    }
                })
            ;
        },

        //扩展文章列表
        appendPostList: function (item) {
            var
                post_url = item.post_url,
                post_title = item.post_title,
                post_category_name = item.post_category_name,
                post_abstract = item.post_abstract,
                post_create_date = item.post_create_date,
                post_views = item.post_views,
                postListContainer = $("#postList .ui.stackable.grid"),
                postListDom = "<div class=\"ui row\">\n" +
                    "                <div class=\"four wide column\">\n" +
                    "                    <time>" + post_create_date + "</time>\n" +
                    "                    <p class=\"category\">" + post_category_name + "</p>\n" +
                    "                </div>\n" +
                    "                <div class=\"eleven wide column\">\n" +
                    "                    <h3><a href=\"" + post_url + "\">" + post_title + "</a></h3>\n" +
                    "                    <div>" + post_abstract + "</div>\n" +
                    "                    <h4 class=\"ui horizontal header divider\">\n" +
                    "                        <a href=\"" + post_url + "\">Read More »</a>\n" +
                    "                    </h4>\n" +
                    "                </div>\n" +
                    "            </div>";
            postListContainer
                .append(postListDom)
            ;
        },

        //加载文章列表
        loadPostList: function ($button, loadPostCount = 5) {
            var index = 0,
                postCount = 0,
                apiURL = "/api/getpostlist";
            $button
                .click(function () {
                    $.getJSON({
                        url: apiURL,
                        type: 'get',
                        data: {
                            'index': index,
                            'count': loadPostCount
                        },
                        success: function (data) {
                            postCount = data.post_count;
                            var postList = data.post_list;
                            $.each(postList, function (i, item) {
                                if (index < postCount) {
                                    index += 1;
                                    blog.handler.appendPostList(item);
                                    $button
                                        .removeClass('hidden')
                                    ;
                                }
                                if (postList.length === 0 || index === postCount)
                                    $button
                                        .addClass('hidden')
                                    ;
                            });
                        }
                    });
                })
                .click()
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

    };

    var ready = function () {
        var
            $sidebar = $(".ui.sidebar"),
            $fixMenu = $('.ui.fixed.menu'),
            $masthead = $("header.masthead");

        //sidebar的展开和折叠
        $sidebar
            .sidebar('attach events', '.expand.item')
        ;

        //顶部导航栏
        $masthead
            .visibility({
                once: false,
                onBottomPassed: function () {
                    $fixMenu.transition('fade in');
                },
                onBottomPassedReverse: function () {
                    $fixMenu.transition('fade out');
                }
            })
        ;
    };
    $(function () {
        ready();
    });
})();

//blog-detail
// (function () {
//     "use strict";
//
//     hljs.initHighlightingOnLoad(); //初始化代码块
//
//     function initToc() {
//         //初始化文章目录
//         let navSelector = "#toc",
//             toc = $(navSelector),
//             body = $("body"),
//             postCommentDivider = $("#post-comment-divider"),
//             sidebar = $("#sidebar"),
//             fadeInTime = 300,
//             fadeOutTime = 300;
//
//         Toc.init(toc);
//         body.scrollspy({
//             target: navSelector
//         });
//
//         $(window).scroll(function () {
//             //侧边栏滚动监听
//             if ($(this).scrollTop() > postCommentDivider.offset().top) {
//                 sidebar.fadeOut(fadeOutTime);
//             } else {
//                 sidebar.fadeIn(fadeInTime);
//             }
//         }).scroll();
//     }
//
//     function initCommentForm() {
//         //初始化评论表单
//         let replaceTextarea = function (textareaId) {
//             //替换文本框为富文本编辑器
//             if ($("#" + textareaId).length > 0) {
//                 let comment_editor = CKEDITOR.replace(textareaId);
//                 comment_editor.on('required', function (evt) {
//                     alert('请填写评论');
//                     evt.cancel();
//                 });
//             }
//         };
//         replaceTextarea('modal_comment_body');
//         replaceTextarea('comment_body');
//
//         let commentModal = $('#commentModal');
//         commentModal.on('show.bs.modal', function (event) {
//             let button = $(event.relatedTarget),
//                 postId = button.data('postid'),
//                 replyUsername = button.data('replyusername'),
//                 parentCommentId = button.data('parentcommentid'),
//                 modalTitleText = '回复 ' + replyUsername,
//                 action = "/comment/post-comment/" + postId + "/" + parentCommentId,
//                 modal = $(this);
//
//             modal.removeAttr('tabindex');
//             modal.find("form").attr("action", action);
//             modal.find('.modal-title').text(modalTitleText);
//         });
//     }
//
//     function hoverComment() {
//         //处理鼠标悬停评论事件
//         let commentList = $(".comment");
//         commentList.each(function () {
//             $(this).hover(function () {
//                 $(this).find(".comment-toolbar").removeClass("d-none")
//             });
//             $(this).mouseleave(function () {
//                 $(this).find(".comment-toolbar").addClass("d-none")
//             })
//         })
//     }
//
//     $(function () {
//         initCommentForm();
//         initToc();
//         hoverComment();
//     });
// })();