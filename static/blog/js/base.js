(function () {
    "use strict";

    window.blog = {
        handler: {},
        before: {},
        ready: {},
        bootstrap: function () {
            $.each(blog.before, function (key, func) {
                func();
            });

            $(function () {
                $.each(blog.ready, function (key, func) {
                    func();
                });
            });
        }
    };

    blog.handler = {
        //判断是否为IE浏览器
        isIE: function () {
            return !!window.ActiveXObject || "ActiveXObject" in window;
        },

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

        //渲染代码块
        initHighlighting: function () {
            hljs.initHighlightingOnLoad();
        },

        //注销
        logout: function ($button) {
            $button.on("click", function () {
                $button.next("form").find("button[type=submit]").click();
            });
        },
    };

    blog.ready = {
        base: function () {
            var
                $sidebar = $(".ui.sidebar"),
                $logoutButton = $('.logout');


            //sidebar的展开和折叠
            if (!(blog.handler.isIE()))
                $sidebar
                    .sidebar('setting', 'transition', 'overlay')
                    .sidebar('attach events', '.expand.item')
                ;
            else
                $sidebar
                    .sidebar('setting', 'transition', 'overlay')
                    .sidebar('setting', 'dimPage', false)
                    .sidebar('attach events', '.expand.item')
                ;

            blog.handler.logout($logoutButton);
        }
    };

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