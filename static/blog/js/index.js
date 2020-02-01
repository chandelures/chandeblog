(function () {
    "use strict";

    $.extend(blog.handler, {
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
                    "                    <h4 class=\"ui header divider\">\n" +
                    "                    </h4>\n" +
                    "                </div>\n" +
                    "            </div>";
            postListContainer
                .append(postListDom)
            ;
        },

        //加载文章列表
        loadPostList: function ($button, loadPostCount) {
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
    });

    blog.before = {
        base: function () {
            blog.handler.initHighlighting();
        }
    };

    blog.ready.index = function () {
        var
            $toUpButton = $("#toUp"),
            $fixMenu = $('.ui.fixed.menu'),
            $masthead = $("header.masthead"),
            $loadPostListButton = $("#loadPostListButton");

        //顶部导航栏
        $fixMenu
            .addClass("hidden")
        ;
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

        blog.handler.loadPostList($loadPostListButton, 5);

        blog.handler.toUp($toUpButton);

    };

    blog.bootstrap();
})();