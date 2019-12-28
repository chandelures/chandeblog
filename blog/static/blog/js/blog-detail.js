hljs.initHighlightingOnLoad(); //初始化代码块
function initToc() {
    //初始化文章目录
    let navSelector = "#toc";
    let $toc = $(navSelector);
    Toc.init($toc);
    $("body").scrollspy({
        target: navSelector
    });
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
        modal.find('.modal-title').text('回复给 ' + replyUsername);
    });

    let replaceTextarea = function (textareaId) {
        //替换文本框为富文本编辑器
        let comment_editor = CKEDITOR.replace(textareaId);
        comment_editor.on('required', function (evt) {
            alert('请填写评论');
            evt.cancel();
        });
    };

    replaceTextarea('modal_comment_body');
    replaceTextarea('comment_body');

}

$(function () {
    initCommentForm();
    initToc()
});