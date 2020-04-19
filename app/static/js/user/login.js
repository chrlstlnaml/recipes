function login() {
    if ($('#loginForm').valid()){
        $('#loginBtn').attr("disabled", "true");
        let myForms = $('#loginForm');
        let formData = new FormData(myForms[0]);

        $.ajax({
            url: '../user/login',
            type: 'POST',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: formData,
            success: function (response) {
                if (response['result_code'] != 200) {
                    $('#loginMessage').text(response['error']);
                    $('#loginMessage').css('display', 'block');
                    $('#loginBtn').removeAttr("disabled");
                } else {
                    $('#loginMessage').css('display', 'none');
                    location='../';
                }
            }
        });
    }
}

