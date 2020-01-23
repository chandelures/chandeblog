(function () {
    "use strict";


    var ready = function () {
        var $uiSticky = $(".ui.sticky"),
            $loadPostListButton = $("#loadPostListButton");

        var handler = {
            loadPostList: function ($button, loadPostCount) {
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
                                            "                    <h3>" + post_title + "</h3>\n" +
                                            "                    <p>" + post_abstract + "</p>\n" +
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

        handler.loadPostList($loadPostListButton, 5);

        $uiSticky
            .sticky({
                context: '#postList'
            })
        ;
    };

    $(function () {
        ready();
    });
})();