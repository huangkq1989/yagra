var request_root = $("#request_root").val();

$(document).ready(function() {
    window.onbeforeunload = function() {
        postReq(request_root + '/app.py/signout', {}, null);
    }
});

var error_handler = function (xhr, textStatus, errorThrown) {
    if(xhr.responseText != null && xhr.responseText != "") {
        var data = xhr.responseText;
        try {
            alert(data);
            alert(JSON.parse(data)["descript"]);
        } catch(e) {
            alert("(" + textStatus + ") " + errorThrown);
        }
    } else {
        alert("(" + textStatus + ") " + errorThrown);
    }
}

var uploadAvatar = function() {
    var form_data = new FormData($('#upload-file')[0]);
    $.ajax({
        type: 'POST',
        url: request_root + '/app.py/upload',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
            var result = eval(data);
            if(result['code'] != 400) {
                $("#upload-info").html(result['descript']);
                return false;
            } else {
                $("#upload-info").html(result['data']['info']);
                $("#alert").attr('class', 'alert alert-info alert-size');
                $("#image").attr('src', result['data']['img']);
            }
            return true;
        },
        error: error_handler,
    });
}
