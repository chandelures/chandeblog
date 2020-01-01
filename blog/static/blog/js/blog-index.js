(function () {
    "use strict";

    hljs.initHighlightingOnLoad(); //初始化代码块

    function loadPostCard() {
        const loadPostCount = 5;

        let index = 0,
            postCount = 0,
            apiUrl = "/api/getpostlist",
            loadPostCardButton = $('#load-post-card');

        loadPostCardButton.click(function () {
            $.getJSON({
                url: apiUrl,
                type: 'get',
                data: {
                    "index": index,
                    'count': loadPostCount
                },
                success: function (ret) {
                    $.each(ret, function (i, item) {
                        postCount = item["post_count"];
                        if (index < postCount) {
                            index += 1;
                            let post_url = item["post_url"],
                                post_title = item["post_title"],
                                post_category_name = item["post_category_name"],
                                post_abstract = item["post_abstract"],
                                post_create_date = item["post_create_date"],
                                post_views = item["post_views"],
                                postCardContainer = $("#post-card-container"),
                                postCardDom = "<div class=\"post-card p-2 pt-5 pb-5\">\n" +
                                    "                        <div class=\"post-card-header text-center\">\n" +
                                    "                            <h2><a href=\"" + post_url + "\"\n" +
                                    "                                   class=\"font-weight-bold text-decoration-none\">" + post_title + "</a></h2>\n" +
                                    "                            <small class=\"text-muted mb-2 pt-2 pb-2\">\n" +
                                    "                                <span><i class=\"fa fa-calendar-o\" aria-hidden=\"true\"></i> " + post_create_date + "</span>\n" +
                                    "                                 <span class=\"pl-1 pr-1\">|</span>\n" +
                                    "                                 <span><i class=\"fa fa-file\"\n" +
                                    "                                                                                 aria-hidden=\"true\"></i> " + post_category_name + "</span>\n" +
                                    "                                 <span class=\"pl-1 pr-1\">|</span>\n" +
                                    "                                <span><i class=\"fa fa-eye\" aria-hidden=\"true\"></i> " + post_views + "</span>\n" +
                                    "                            </small>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"post-card-abstract post-markdown pb-3 pt-3 text-white\">\n" + post_abstract +
                                    "                        </div>\n" +
                                    "                        <div class=\"post-card-footer text-center\">\n" +
                                    "                            <a class=\"text-decoration-none p-2 border font-weight-bold\" href=\"" + post_url + "\">阅读全文 »</a>\n" +
                                    "                            <div class=\"post-card-divider\"></div>\n" +
                                    "                        </div>\n" +
                                    "                    </div>";
                            postCardContainer.append(postCardDom);
                            loadPostCardButton.removeClass('d-none');
                        }
                    });
                    if (ret.length === 0 || index === postCount)
                        loadPostCardButton.addClass('d-none');
                }
            });
        }).click();
    }

    $(function () {
        loadPostCard();
    });
})();