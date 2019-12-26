$(function () {
    function scollToc() {
        let navSelector = "#toc";
        let $toc = $(navSelector);
        Toc.init($toc);
        $("body").scrollspy({
            target: navSelector
        });
    }

    function initCommentForm() {
        $('#commentModal').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let postId = button.data('postid');
            let replyUsername = button.data('replyusername');
            let parentCommentId = button.data('parentcommentid');
            let modal = $(this);
            modal.find("form").attr("action", "/comment/post-comment/" + postId + "/" + parentCommentId);
            modal.find('.modal-title').text('回复给 ' + replyUsername);
        });
        ClassicEditor
            .create(document.querySelector('#modal_comment_body'), {
                toolbar: ['bold', 'numberedList'],
            })
            .catch(error => {
                console.error(error);
            });
        ClassicEditor
            .create(document.querySelector('#comment_body'), {
                toolbar: ['bold', 'numberedList'],
            })
            .catch(error => {
                console.error(error);
            });
    }

    initCommentForm();
    scollToc()
});