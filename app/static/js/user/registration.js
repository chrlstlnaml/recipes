var isValidPassw = false;

function signUp() {
    $('#signUpForm').validate({
        rules: {
            password: {
                validateFigure: $('#password').val(),
            }
        }
    });
    if ($('#signUpForm').valid()){
        if (isValidPassw) {
            $('#signUpBtn').attr("disabled", "true");
            let myForms = $('#signUpForm');
            let formData = new FormData(myForms[0]);

            $.ajax({
                url: '../user/sign_up',
                type: 'POST',
                contentType: false,
                processData: false,
                dataType: 'json',
                data: formData,
                success: function (response) {
                    if (response['result_code'] != 200) {
                        $('#signUpMessage').removeClass();
                        $('#signUpMessage').addClass('alert alert-danger');
                        $('#signUpMessage').text(response['error']);
                        $('#signUpMessage').css('display', 'block');
                        $('#signUpBtn').removeAttr("disabled");
                    } else {
                        $('#signUpMessage').removeClass();
                        $('#signUpMessage').addClass('alert alert-info');
                        $('#signUpMessage').text(response['message']);
                        $('#signUpMessage').css('display', 'block');
                        window.setTimeout(function () {
                            window.location.href = "/";
                        }, 2000);
                    }
                }
            });
        } else {
            $('.btn').attr('disabled', 'true');
            $('#password2').css('border-color', 'red');
        }
    }
}


function checkPassword() {
    if ($('#password').val() == $('#password2').val()) {
        $('.btn').removeAttr('disabled');
        isValidPassw = true;
        if ($('#password').val().length >= 6) $('#password2').css('border-color', '#ccc');
    } else {
        $('.btn').attr('disabled', 'true');
        $('#password2').css('border-color', 'red');
        isValidPassw = false;
    }
}

function fillInLogin(email) {
    if (!$('#login').val()) {
        if (email.search('@') != -1) {
            $('#login').val(email.split('@')[0])
        }
    }
}

$.validator.addMethod('validateFigure',
    function (val) {
        return !!((/[0-9]/.test(val)) && (val.match(/[A-Z]/g)));
    }, "Пароль должен содержать минимум одну цифру и одну заглавную букву");