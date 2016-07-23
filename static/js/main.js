function correct_message() {
    $('.correct_msg').click(function() {
        var $list = $(this).parent().parent();
        var $msg = $list.find('p.content:first');
        var $textarea = $list.find('.content-correct:first');

        $('.content-correct').hide();
        $(".comment").hide();

        $msg.hide();
        $textarea.find('#id_content_correct').val($msg.text());
        $textarea.show();
    });
}

function comment_message() {
    $(".addcomment").click(function() {
        var msg_id = $(this).attr('data-comment-id');

        $('.content-correct').hide();
        $(".comment").hide();
        $('.content').show();
//        $(this).next().next().show();

        $(("#comment_to").concat(msg_id)).toggle();
    });
}

$(document).ready(function() {
    correct_message();
    comment_message();
});