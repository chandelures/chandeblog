(function () {
    "use strict";

    var ready = function () {
        var $tocSticky = $(".post-detail .ui.sticky"),
            $toUpButton = $("#toUp"),
            $loadPostListButton = $("#loadPostListButton");

        var loadPostCount = 5;

        var handler = {
            toUp: function ($button) {
                var fadeInTime = 300,
                    fadeOutTime = 300,
                    scrollSpace = 300,
                    animateTime = 500;
                $button.click(function () {
                    $('html,body').animate({scrollTop: 0}, animateTime);
                });
                $(window).scroll(function () {
                    if ($(this).scrollTop() > scrollSpace) {
                        $button.fadeIn(fadeInTime);
                    } else {
                        $button.stop().fadeOut(fadeOutTime);
                    }
                }).scroll();

            },
            loadPostList: function ($button, loadPostCount = 5) {
                var index = 0,
                    postCount = 0,
                    apiURL = "/api/getpostlist";

                $button.click(function () {
                    $.getJSON({
                        url: apiURL,
                        type: 'get',
                        data: {
                            "index": index,
                            'count': loadPostCount
                        },
                        success: function (data) {
                            postCount = data.post_count;
                            var postList = data.post_list;
                            $.each(postList, function (i, item) {
                                if (index < postCount) {
                                    index += 1;
                                    var post_url = item.post_url,
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
                                    postListContainer.append(postListDom);
                                    $button.removeClass('hidden');
                                }
                                if (postList.length === 0 || index === postCount)
                                    $button.addClass('hidden');
                            });
                        }
                    });
                }).click();
            }
        };

        handler.loadPostList($loadPostListButton, loadPostCount);
        handler.toUp($toUpButton);

        $tocSticky
            .sticky({
                context: '#postDetail'
            })
        ;
    };

    hljs.initHighlightingOnLoad();

    $(function () {
        ready();
    });
})();