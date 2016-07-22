function correct_message() {
    $('.content-correct').hide();
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

function putP() {
    $('textarea').html('<pre></pre>');
}


$(document).ready(function() {
    correct_message();
    $(".comment").hide();
    $(".addcomment").click(function() {
        var msg_id = $(this).attr('data-comment-id');
//        var li = $(this).parent().parent();

        $('.content-correct').hide();
        $(".comment").hide();
//        $(this).next().next().show();

        $(("#comment_to").concat(msg_id)).toggle();

//        li.toggleClass('active');
    });
});