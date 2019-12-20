$(function () {
    function load_post_card(load_post_count = 2) {
        let index = 0;
        let post_count = 0;
        let api_url = "/api/getpostlist";

        function append_container(item) {
            $("#post-card-container").append("<div class=\"post-card p-3\">\n" +
                "                        <div class=\"post-card-header\">\n" +
                "                            <div class=\"dropdown-divider pb-5\"></div>\n" +
                "                            <h2><a href=\"#\" class=\"text-decoration-none\">" + item["post_title"] + "</a></h2>\n" +
                "                            <p class=\"text-white mb-2 pt-2 pb-2\">\n" +
                "                                <span class=\"text-dark bg-white badge\">" + item["post_create_date"] + "</span>\n" +
                "                                <a href=\"#\"><span class=\"badge bg-white text-dark ml-2\">" + item["post_category_name"] + "</span></a>\n" +
                "                            </p>\n" +
                "                        </div>\n" +
                "                        <div class=\"post-card-abstract pb-3\">\n" +
                "                            <p class=\"lead text-white\">\n" +
                "                                <i class=\"fa fa-quote-left\" aria-hidden=\"true\"></i>\n" +
                "                                " + item["post_abstract"] + "\n" +
                "                            </p>\n" +
                "                        </div>\n" +
                "                        <div class=\"post-card-read-more text-center mt-3 mb-3\">\n" +
                "                            <button class=\"btn\">READ MORE</button>\n" +
                "                        </div>\n" +
                "                    </div>");
        }

        function get_data() {
            $.getJSON({
                url: api_url,
                type: 'get',
                data: {
                    "index": index,
                    'count': load_post_count
                },
                success: function (ret) {
                    $.each(ret, function (i, item) {
                        post_count = item["post_count"];
                        if (index < post_count) {
                            index += 1;
                            append_container(item)
                        }
                    });
                    if (ret.length === 0 || index === post_count)
                        $("#load-post-card").remove();
                }
            });
        }

        $("#load-post-card").click(function () {
            get_data();
        }).click();
    }

    load_post_card()
});