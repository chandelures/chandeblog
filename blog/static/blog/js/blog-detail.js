$(function () {
    function scollToc() {
        let navSelector = "#toc";
        let $toc = $(navSelector);
        Toc.init($toc);
        $("body").scrollspy({
            target: navSelector
        });
    }

    scollToc()
});