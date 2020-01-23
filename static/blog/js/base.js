(function () {
    "use strict";
    var ready = function () {
        var
            $sidebar = $(".ui.sidebar"),
            $fixMenu = $('.ui.fixed.menu'),
            $masthead = $("header.masthead");

        //sidebar的展开和折叠
        $sidebar
            .sidebar('attach events', '.toc.item')
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
// (function () {
//     "use strict";
//
//     function toUpButtonInit() {
//         let button = $('#toUp');
//         let fadeInTime = 300,
//             fadeOutTime = 300,
//             scrollSpace = 300,
//             animateTime = 500;
//         button.click(function () {
//             $('html,body').animate({scrollTop: 0}, animateTime);
//         });
//         $(window).scroll(function () {
//             if ($(this).scrollTop() > scrollSpace) {
//                 button.fadeIn(fadeInTime);
//             } else {
//                 button.stop().fadeOut(fadeOutTime);
//             }
//         }).scroll();
//     }
//
//     $(function () {
//         toUpButtonInit();
//     });
// })();

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

//blog-index
// (function () {
//     "use strict";
//
//     hljs.initHighlightingOnLoad(); //初始化代码块
//
//     function loadPostCard() {
//         const loadPostCount = 5;
//
//         let index = 0,
//             postCount = 0,
//             apiUrl = "/api/getpostlist",
//             loadPostCardButton = $('#load-post-card');
//
//         loadPostCardButton.click(function () {
//             $.getJSON({
//                 url: apiUrl,
//                 type: 'get',
//                 data: {
//                     "index": index,
//                     'count': loadPostCount
//                 },
//                 success: function (data) {
//                     postCount = data["post_count"];
//                     let postList = data["post_list"];
//                     $.each(postList, function (i, item) {
//                         if (index < postCount) {
//                             index += 1;
//                             let post_url = item["post_url"],
//                                 post_title = item["post_title"],
//                                 post_category_name = item["post_category_name"],
//                                 post_abstract = item["post_abstract"],
//                                 post_create_date = item["post_create_date"],
//                                 post_views = item["post_views"],
//                                 postCardContainer = $("#post-card-container"),
//                                 postCardDom = "<div class=\"post-card p-2 pt-5 pb-5\">\n" +
//                                     "                        <div class=\"post-card-header text-center\">\n" +
//                                     "                            <h2><a href=\"" + post_url + "\"\n" +
//                                     "                                   class=\"font-weight-bold text-decoration-none\">" + post_title + "</a></h2>\n" +
//                                     "                            <small class=\"text-muted mb-2 pt-2 pb-2\">\n" +
//                                     "                                <span><i class=\"fa fa-calendar-o\" aria-hidden=\"true\"></i> " + post_create_date + "</span>\n" +
//                                     "                                 <span class=\"pl-1 pr-1\">|</span>\n" +
//                                     "                                 <span><i class=\"fa fa-file\"\n" +
//                                     "                                                                                 aria-hidden=\"true\"></i> " + post_category_name + "</span>\n" +
//                                     "                                 <span class=\"pl-1 pr-1\">|</span>\n" +
//                                     "                                <span><i class=\"fa fa-eye\" aria-hidden=\"true\"></i> " + post_views + "</span>\n" +
//                                     "                            </small>\n" +
//                                     "                        </div>\n" +
//                                     "                        <div class=\"post-card-abstract post-markdown pb-3 pt-3 text-white\">\n" + post_abstract +
//                                     "                        </div>\n" +
//                                     "                        <div class=\"post-card-footer text-center\">\n" +
//                                     "                            <a class=\"text-decoration-none p-2 border font-weight-bold\" href=\"" + post_url + "\">阅读全文 »</a>\n" +
//                                     "                            <div class=\"post-card-divider\"></div>\n" +
//                                     "                        </div>\n" +
//                                     "                    </div>";
//                             postCardContainer.append(postCardDom);
//                             loadPostCardButton.removeClass('d-none');
//                         }
//                         if (postList.length === 0 || index === postCount)
//                             loadPostCardButton.addClass('d-none');
//                     });
//                 }
//             });
//         }).click();
//     }
//
//     $(function () {
//         loadPostCard();
//     });
// })
// ();