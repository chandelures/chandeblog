(function () {
    var ready = function () {
        var
            $sidebar = $(".ui.sidebar");
        $sidebar
            .sidebar('attach events', '.toc.item')
        ;
    };
    $(function () {
        ready();
    });
})();