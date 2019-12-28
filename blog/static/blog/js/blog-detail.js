hljs.initHighlightingOnLoad(); //初始化代码块
function initToc() {
    //初始化文章目录
    let navSelector = "#toc",
        $toc = $(navSelector),
        fadeInTime = 300,
        fadeOutTime = 300;

    Toc.init($toc);
    $("body").scrollspy({
        target: navSelector
    });

    $(window).scroll(function () {
        //侧边栏滚动监听
        if ($(this).scrollTop() > $("#post-comment-divider").offset().top) {
            $('#sidebar').fadeOut(fadeOutTime);
        } else {
            $('#sidebar').fadeIn(fadeInTime);
        }
    }).scroll();
}

function initCommentForm() {
    //初始化评论表单
    $('#commentModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let postId = button.data('postid');
        let replyUsername = button.data('replyusername');
        let parentCommentId = button.data('parentcommentid');
        let modal = $(this);
        modal.find("form").attr("action", "/comment/post-comment/" + postId + "/" + parentCommentId);
        modal.find('.modal-title').text('回复 ' + replyUsername);
    });

    let replaceTextarea = function (textareaId) {
        //替换文本框为富文本编辑器
        if ($("#" + textareaId).length > 0) {
            let comment_editor = CKEDITOR.replace(textareaId);
            comment_editor.on('required', function (evt) {
                alert('请填写评论');
                evt.cancel();
            });
        }
    };

    replaceTextarea('modal_comment_body');
    replaceTextarea('comment_body');

}

$(function () {
    initCommentForm();
    initToc()
});