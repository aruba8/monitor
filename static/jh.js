$(function(){
    $("#dialog-confirm").css('display', 'none');
    var removeButton = $('.remove');
    var editButton = $('.edit');

    removeButton.click(function(){
        var histId = $(this).attr('name');
        $( "#dialog-confirm" ).dialog({
            resizable: true,
            height: 205,
            width: 560,
            modal: true,
            buttons: {
                "Delete host": function() {
                    removeHost(histId);
                    $( this ).dialog( "close" );
                },
                "Cancel": function() {
                    $( this ).dialog( "close" );
                }
            }
        });

    });

    function removeHost(hostId){
        $.ajax({
            dataType: "json",
            url: '/admin/hosts',
            data: {
                "host_to_delete": hostId
            },
            type: 'POST',
            complete: function(data){
                location.reload(true);
            }
        });
    }

    editButton.click(function(){
        var editForm = $('#edit-form');
        var offset = $(this).offset();
        var hostId = $(this).attr("name");
        var hostInput = $("#edit-host-field");
        var xpathInput = $("#edit-xpath-field");
        var editInput = $("#edit-input");

        editForm.css("top", offset.top - 88);
        editForm.css("left", offset.left - 450);

        $.post("/admin/hosts", {getHostId: hostId}, function(res){
            var host = res.host;
            var xpath = res.xpath;
            hostInput.val(host);
            xpathInput.val(xpath);
            editInput.attr("value",hostId);

        }, "json");
        editForm.show();
    });

});