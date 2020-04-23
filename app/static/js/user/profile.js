function updatePhoto(photo) {
    if (photo.files[0].size > fileSize) {
        $('#profileMessage').text('Вес файла не должен превышать ' + fileSize + 'кб.');
        $('#profileMessage').css('display', 'block');
    } else {
        let myForms = $('#updatePhotoForm');
        let formData = new FormData(myForms[0]);
        $('.btn').attr('disabled', 'disabled');
        $.ajax({
            url: '../user/update_photo',
            type: 'POST',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: formData,
            success: function (response) {
                if (response['result_code'] == 200) {
                    setTimeout('location="../user/profile";', 1000);
                } else {
                    $('#profileMessage').text(response['error']);
                    $('#profileMessage').css('display', 'block');
                    $('.btn').removeAttr('disabled');
                }
            }
        });
    }
}


function deletePhoto() {
    $('.btn').attr('disabled', 'disabled');
    $.ajax({
        url: '../user/delete_photo',
        type: 'DELETE',
        contentType: false,
        processData: false,
        dataType: 'json',
        success: function (response) {
            if (response['result_code'] == 200) {
                setTimeout('location="../user/profile";', 1000);
            } else {
                $('#profileMessage').text(response['error']);
                $('#profileMessage').css('display', 'block');
                $('.btn').removeAttr('disabled');
            }
        }
    });
}

function saveProfile() {
    if ($('#profileForm').valid()) {
        $('.btn').attr('disabled', 'disabled');
        let myForms = $('#profileForm');
        let formData = new FormData(myForms[0]);
        $.ajax({
            url: '../user/save_profile',
            type: 'PUT',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: formData,
            success: function (response) {
                if (response['result_code'] == 200) {
                    setTimeout('location="../user/profile";', 1000);
                } else {
                    $('#profileMessage').text(response['error']);
                    $('#profileMessage').css('display', 'block');
                    $('.btn').removeAttr('disabled');
                }
            }
        });
    }
}


function changePassword() {
    $('#changePasswordForm').validate({
        rules: {
            password: {
                validateFigure: $('#password').val(),
            }
        }
    });
    if ($('#changePasswordForm').valid()) {
        $('.btn').attr('disabled', 'disabled');
        let myForms = $('#changePasswordForm');
        let formData = new FormData(myForms[0]);
        $.ajax({
            url: '../user/change_password',
            type: 'PUT',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: formData,
            success: function (response) {
                if (response['result_code'] == 200) {
                    setTimeout('location="../user/profile";', 1000);
                } else {
                    $('#changePasswordMessage').text(response['error']);
                    $('#changePasswordMessage').css('display', 'block');
                    $('.btn').removeAttr('disabled');
                }
            }
        });
    }
}

function checkPassword() {
    if ($('#password').val() == $('#password2').val()) {
        $('#savePasswBtn').removeAttr('disabled');
        if ($('#password').val().length >= 6) $('#password2').css('border-color', '#ccc');
    } else {
        $('#savePasswBtn').attr('disabled', 'true');
        $('#password2').css('border-color', 'red');
    }
}

$.validator.addMethod('validateFigure',
    function (val) {
        return !!((/[0-9]/.test(val)) && (val.match(/[A-Z]/g)));
    }, "Пароль должен содержать минимум одну цифру и одну заглавную букву");