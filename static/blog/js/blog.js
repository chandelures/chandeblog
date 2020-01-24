(function () {
    "use strict";

    var ready = function () {
        var
            $tocContainer = $(".post-detail .overlay"),
            $toc = $tocContainer.find(".toc"),
            $postDetail = $("#postDetail"),
            $toUpButton = $("#toUp"),
            $loadPostListButton = $("#loadPostListButton");

        var loadPostCount = 5;

        var handler = {
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
                        $('html,body').scrollTop($(target).offset().top - offset + 1);
                    })
                ;
                $window
                    .scroll(function () {
                        $h.each(function () {
                                var $this = $(this);
                                if (this.tagName === "H2") {
                                    if ($window.scrollTop() > $this.offset().top - offset) {
                                        handler.deactiveAnchor($toc, 1);
                                        handler.activeAnchor($this);
                                    }
                                } else if (this.tagName === "H3") {
                                    if ($window.scrollTop() > $this.offset().top - offset) {
                                        handler.deactiveAnchor($toc, 2);
                                        handler.activeAnchor($this);
                                    }
                                }
                            }
                        );
                        if (handler.isArriveBottom()) {
                            var last = $h[$h.length - 1];
                            if (last.tagName === "H2") {
                                handler.deactiveAnchor($toc, 1);
                                handler.activeAnchor($(last));
                            } else if (last.tagName === "H3") {
                                handler.deactiveAnchor($toc, 2);
                                handler.activeAnchor($(last));
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
                                        handler.appendPostList(item);
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
            }
        };

        handler.loadPostList($loadPostListButton, loadPostCount);

        handler.toUp($toUpButton);

        handler.initToc($toc, $postDetail);

        $tocContainer
            .visibility({
                type: 'fixed',
                offset: 75
            })
        ;
    };

    hljs.initHighlightingOnLoad();

    $(function () {
        ready();
    });
})();