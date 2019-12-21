$(function () {
    let fadeInTime = 300;
    let fadeOutTime = 300;
    let scroll = 300;
    let animateTime = 500;
    function toUp(fadeInTime, fadeOutTime, scroll, animateTime) {
        $('#toUp').click(function () {
            $('html,body').animate({scrollTop: 0}, animateTime);
        });
        $(window).scroll(function () {
            if ($(this).scrollTop() > scroll) {
                $('#toUp').fadeIn(fadeInTime);
            } else {
                $('#toUp').stop().fadeOut(fadeOutTime);
            }
        }).scroll();
    }

    toUp(fadeInTime, fadeOutTime, scroll, animateTime)
});