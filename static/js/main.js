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

        $(("#comment_to").concat(msg_id)).toggle();
    });
}

function infinityScroll() {
	var sign_end = false;
	var $l_m = $('#load_more');
	var ajax_call_running = false;
	var num_page = parseInt($l_m.data('num-pages'), 10);
    var page_number = parseInt($l_m.data('page'), 10);
    var url_to_go;

	$(window).endlessScroll({
		inflowPixels: 300,
		callback: function() {
			if ( ajax_call_running ) {
                return;
            }

            ajax_call_running = true;

			// if it is not all objects
			if ( sign_end == false ) {
				url_to_go = ("/board/?page=").concat(page_number + 1);

				$.ajax({
					url: url_to_go,
					dataType: 'html',
					beforeSend: function() {
					    $('#loading').show();
					},
					success: function(html) {
						var html = $(html);
						var rows = html.find('#notice_list').children();

						page_number = html.find('#load_more').data('page');

						$l_m.data("page", page_number);
						$('#notice_list').append(rows);
						$('#loading').hide();
						if ( page_number >= num_page ) {
							sign_end = true;
						}
						correct_message();
						comment_message();

						ajax_call_running = false;
					},
					error: function() {
					    alert('Error durin scrolling ...');
					    ajax_call_running = false;
					    $('#loading').hide();
					}
				});
			}
		}
	});
}

$(document).ready(function() {
    correct_message();
    comment_message();
    infinityScroll();
});