(function () {
    var ready = function () {
        var
            $sidebar = $(".ui.sidebar"),
            $fixMenu = $('.ui.fixed.menu'),
            $masthead = $("header.masthead");

        //sidebar的展开和折叠
        $sidebar
            .sidebar('attach events', '.toc.item')
        ;

        //顶部导航栏
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
    };
    $(function () {
        ready();
    });
})();