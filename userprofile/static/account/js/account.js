function initForm() {
    $("main form input").each(function () {
        if($(this).attr("type") === "checkbox")
            $(this).addClass("form-check-input");
        else $(this).addClass("form-control");
    })
}

$(function () {
    initForm()
});