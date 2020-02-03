(function () {
    "use strict";

    $.extend(blog.handler, {
        initSearchInput: function ($input) {
            $input
                .addClass("prompt")
                .attr("type", "text")
                .attr("placeholder", "Search...")
            ;
        }
    });

    blog.before = {
        base: function () {
            var
                $searchInput = $(".search.form input");

            blog.handler.initSearchInput($searchInput);
        }
    };

    blog.ready.search = function () {

    };

    blog.bootstrap();
})();