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