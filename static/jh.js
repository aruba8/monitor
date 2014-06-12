$(function(){
    var removeButton = $('.remove');
    var editButton = $('.edit');
    var hider = $('#hider');

    hider.hide();

    removeButton.click(function(){
        var removeForm = $("#delete-form");
        var offset = $(this).offset();
        var hostId = $(this).attr("name");
        var okButton = $("#delete-submit");
        var cancelButton = $("#delete-cancel");
        removeForm.css("top", offset.top - 0);
        removeForm.css("left", offset.left - 450);
        okButton.click(function(){
            removeHost(hostId);
            hider.fadeOut('slow');
        });   
        cancelButton.click(function(){
            removeForm.hide();
            hider.fadeOut('slow');
        })
        hider.fadeIn("slow");
        removeForm.show();
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
        var cancelButton = $('#cancel-edit');

        editForm.css("top", offset.top - 88);
        editForm.css("left", offset.left - 450);

        $.post("/admin/hosts", {getHostId: hostId}, function(res){
            var host = res.host;
            var xpath = res.xpath;
            hostInput.val(host);
            xpathInput.val(xpath);
            editInput.attr("value",hostId);

        }, "json");

        cancelButton.click(function(){
            hider.fadeOut('slow');
            editForm.hide();
        });
        hider.fadeIn("slow");
        editForm.show();
    });

});