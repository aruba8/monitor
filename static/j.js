$(function(){
    var hider = $('#hider');
    hider.hide();

    $('.remove-link').click(function(){
        var removeForm = $("#delete-form");
        var offset = $(this).offset();
        var urlId = $(this).attr("name");
        var okButton = $("#delete-submit");
        var cancelButton = $("#delete-cancel");
        removeForm.css("top", offset.top - 85);
        removeForm.css("left", offset.left - 300);
        okButton.click(function(){
            removeUrl(urlId);
            hider.fadeOut('slow');
        });   
        cancelButton.click(function(){
            removeForm.hide();
            hider.fadeOut('slow');
        });
        hider.fadeIn("slow");
        removeForm.show();
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
