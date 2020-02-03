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
                $search = $(".ui.search"),
                $logoutButton = $('.logout');

            $search.each(function () {
                $(this)
                    .search({
                        apiSettings: {
                            url: '/api/search/repositories?q={query}'
                        },
                    })
                ;
            });


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