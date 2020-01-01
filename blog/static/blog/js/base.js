(function () {
    "use strict";

    function toUpButtonInit() {
        let button = $('#toUp');
        let fadeInTime = 300,
            fadeOutTime = 300,
            scrollSpace = 300,
            animateTime = 500;
        button.click(function () {
            $('html,body').animate({scrollTop: 0}, animateTime);
        });
        $(window).scroll(function () {
            if ($(this).scrollTop() > scrollSpace) {
                button.fadeIn(fadeInTime);
            } else {
                button.stop().fadeOut(fadeOutTime);
            }
        }).scroll();
    }

    $(function () {
        toUpButtonInit()
    });
})();