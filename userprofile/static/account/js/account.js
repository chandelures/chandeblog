function initForm() {
    let form = $("main form");
    form.find("input").each(function () {
        if ($(this).attr("type") === "checkbox") {
            $(this).addClass("form-check-input");
        } else {
            $(this).addClass("form-control").removeAttr("placeholder");
        }
    });
    form.find("textarea").each(function () {
        $(this).addClass("form-control");
    })
}

function avatarChange() {
    $("#avatar_change").click(function () {
        $("#avatar_change_input").click();
    });
    $("#avatar_change_input").change(function () {
        let avatar = $("#avatar_change_input").val();
        if (avatar) {
            let data = new FormData($("#avatar_change_form")[0]);
            $.ajax({
                url: "/accounts/avatar_change/",
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

$(function () {
    avatarChange();
    initForm();
});