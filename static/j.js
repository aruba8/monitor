$(function(){
    $("#dialog-confirm").css('display', 'none');
    $('a.remove-link').click(function(){
        var urlId = $(this).attr('name');
        $( "#dialog-confirm" ).dialog({
            resizable: true,
            height: 205,
            width: 560,
            modal: true,
            buttons: {
                "Delete URL": function() {
                    removeUrl(urlId);
                    $( this ).dialog( "close" );
                },
                "Cancel": function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });

    function removeUrl(urlId){
        $.ajax({
            url: '/admin',
            data: {
                url_to_delete: urlId
            },
            type: 'POST',
            complete: function(data){
                location.reload(true);
            }
        });
    }


});
