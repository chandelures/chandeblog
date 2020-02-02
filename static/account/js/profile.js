(function () {
    $.extend(blog.handler, {
        changeAvatar: function ($avatarChangeForm) {
            var $avatarInput = $avatarChangeForm.find("input");
            $avatarInput.click();
            $avatarInput.change(function () {
                let avatar = $(this).val();
                if (avatar) {
                    let data = new FormData($avatarChangeForm[0]);
                    $.ajax({
                        url: "/api/changeavatar/",
                        type: "POST",
                        data: data,
                        processData: false,
                        contentType: false,
                        dataType: "json",
                        success: function (data, status) {
                            window.location.reload();
                        }
                    });
                }
            });
        }
    });

    blog.ready.profile = function () {
        var
            $changeAvatarButton = $(".change-avatar"),
            $avatarChangeForm = $("form.avatar-change"),
            $cardDimmer = $(".card .dimmer");

        $cardDimmer
            .dimmer({
                on: 'hover'
            })
        ;

        $changeAvatarButton
            .click(function () {
                blog.handler.changeAvatar($avatarChangeForm)
            })
        ;
    };

    blog.bootstrap()
})();