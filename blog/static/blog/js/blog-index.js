function loadPostCard(loadPostCount) {
    let index = 0,
        postCount = 0,
        apiUrl = "/api/getpostlist";

    function append_container(item) {
        let post_url = item["post_url"],
            post_title = item["post_title"],
            post_category_name = item["post_category_name"],
            post_category_url = item["post_category_url"],
            post_abstract = item["post_abstract"],
            post_create_date = item["post_create_date"];
        $("#post-card-container").append("<div class=\"post-card p-3 mt-5\">\n" +
            "                        <div class=\"post-card-header text-center\">\n" +
            "                            <h2><a href=\"" + post_url + "\"\n" +
            "                                   class=\"font-weight-bold text-decoration-none\">" + post_title + "</a></h2>\n" +
            "                            <small class=\"text-muted mb-2 pt-2 pb-2\">\n" +
            "                                <span><i class=\"fa fa-calendar-o\" aria-hidden=\"true\"></i> " + post_create_date + "</span>\n" +
            "                                 <span class=\"pl-1 pr-1\">|</span>\n" +
            "                                <a class=\"text-muted\" href=\"#\"><span><i class=\"fa fa-file\"\n" +
            "                                                                                 aria-hidden=\"true\"></i> " + post_category_name + "</span></a>\n" +
            "                            </small>\n" +
            "                        </div>\n" +
            "                        <div class=\"post-card-abstract post-markdown pb-3 pt-3 text-white\">\n" + post_abstract +
            "                        </div>\n" +
            "                        <div class=\"post-card-footer text-center\">\n" +
            "                            <a class=\"text-decoration-none p-2 border font-weight-bold\" href=\"" + post_url + "\">阅读全文 »</a>\n" +
            "                            <div class=\"post-card-divider pt-5\"></div>\n" +
            "                        </div>\n" +
            "                    </div>");
    }

    function get_data() {
        $.getJSON({
            url: apiUrl,
            type: 'get',
            data: {
                "index": index,
                'count': loadPostCount
            },
            success: function (ret) {
                let loadPostCard = $('#load-post-card');
                $.each(ret, function (i, item) {
                    postCount = item["post_count"];
                    if (index < postCount) {
                        index += 1;
                        append_container(item);
                        loadPostCard.removeClass('d-none');
                    }
                });
                if (ret.length === 0 || index === postCount)
                    loadPostCard.remove();
            }
        });
    }

    $("#load-post-card").click(function () {
        get_data();
    }).click();
}

$(function () {
    let load_post_count = 5;

    loadPostCard(load_post_count);
});