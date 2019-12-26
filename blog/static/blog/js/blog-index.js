$(function () {
    let load_post_count = 2;

    function loadPostCard(loadPostCount) {
        let index = 0;
        let postCount = 0;
        let apiUrl = "/api/getpostlist";

        function append_container(item) {
            let post_url = item["post_url"];
            let post_title = item["post_title"];
            let post_category_name = item["post_category_name"];
            let post_category_url = item["post_category_url"];
            let post_abstract = item["post_abstract"];
            $("#post-card-container").append("<div class=\"post-card p-3\">\n" +
                "                        <div class=\"post-card-header\">\n" +
                "                            <div class=\"dropdown-divider pb-5\"></div>\n" +
                "                            <h2><a href=\"" + post_url + "\" class=\"text-decoration-none font-weight-bold\">" + post_title + "</a></h2>\n" +
                "                            <p class=\"text-white mb-2 pt-2 pb-2\">\n" +
                "                                <span class=\"text-dark bg-white badge\">" + item["post_create_date"] + "</span>\n" +
                "                                <a href=\"" + post_category_url + "\"><span class=\"badge bg-white text-dark ml-2\">" + post_category_name + "</span></a>\n" +
                "                            </p>\n" +
                "                        </div>\n" +
                "                        <div class=\"post-card-abstract pb-3 post-markdown text-white\">\n" +
                "                            <p class=\"lead text-white\">\n" +
                "                                " + post_abstract + "\n" +
                "                            </p>\n" +
                "                        </div>\n" +
                "                        <div class=\"post-card-read-more text-center mt-2 mb-2\">\n" +
                "                            <button class=\"btn\" onclick='window.location.href=\"" + item["post_url"] + "\"'>READ MORE <i class=\"fa fa-arrow-right\" aria-hidden=\"true\"></i></button>\n" +
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
                    $.each(ret, function (i, item) {
                        postCount = item["post_count"];
                        if (index < postCount) {
                            index += 1;
                            append_container(item)
                        }
                    });
                    if (ret.length === 0 || index === postCount)
                        $("#load-post-card").remove();
                }
            });
        }

        $("#load-post-card").click(function () {
            get_data();
        }).click();
    }

    loadPostCard(load_post_count);
});