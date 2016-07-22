//main.js
$(document).ready(function() {
    $(".comment").hide();
    $(".addcomment").click(function() {
        var msg_id = $(this).attr('data-comment-id');
        var li = $(this).parent().parent();


        $(".comment").hide();
//        $(this).next().next().show();

        $(("#comment_to").concat(msg_id)).toggle();

//        li.toggleClass('active');
//        alert($(this).attr('data-comment-id'));
    });
});