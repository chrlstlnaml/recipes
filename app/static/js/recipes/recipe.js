$('.selectpicker-complexity').selectpicker({
    noneSelectedText: 'Выберите сложность'
});

$('.selectpicker-category').selectpicker({
    noneSelectedText: 'Выберите категории'
});

$('#description').summernote({
    height: 300
});

init_selects();

function init_selects() {
    $('.selectpicker-ingredient').selectpicker({
        noneSelectedText: 'Выберите ингридиент'
    });

    $('.selectpicker-measure').selectpicker({
        noneSelectedText: 'Выберите меру измерения'
    });
}


function addIngredient() {
    ingredientIndex++;
    $.ajax({
        url: '../recipes/get_ingredient_html?index=' + ingredientIndex,
        type: 'GET',
        success: function (response) {
            $('#ingredientDiv').append(response);
            init_selects();
        }
    })
}


function delIngredient(ind) {
    $('#divIngredients-' + ind).remove();
}


$('#mNewIngredient').on('show.bs.modal', function (event) {
    let modal = $(this);
    modal.find('#ingredient_name').val('');
});


function saveNewIngredient() {
    if ($('#newIngredientForm').valid()) {
        $('.new-ingredient-btn').attr("disabled", "true");
        let myForms = $('#newIngredientForm');
        let formData = new FormData(myForms[0]);

        $.ajax({
            url: '../recipes/add_ingredient',
            type: 'POST',
            contentType: false,
            processData: false,
            dataType: 'json',
            data: formData,
            success: function (response) {
                if (response['result_code'] == 200) {
                    $('#newIngredientMessage').css('display', 'none');
                    $('.selectpicker-ingredient').append('<option value="' + response['ingredient']['id'] +
                        '">' + response['ingredient']['name'] + '</option>');
                    $(".selectpicker-ingredient").selectpicker("refresh");
                    $('#mNewIngredient').modal('hide');
                } else {
                    $('#newIngredientMessage').text(response['error']);
                    $('#newIngredientMessage').css('display', 'block');
                }
                $('.new-ingredient-btn').removeAttr("disabled");
            }
        });
    }
}


function saveRecipe() {
    if ($('#saveRecipeForm').valid()) {
        let myForms = $('#saveRecipeForm');
        let formData = new FormData(myForms[0]);
        if (!$("#photo").val() || ($("#photo").val() && $("#photo").prop('files')[0].size <= fileSize)) {
            $('.btn').attr("disabled", "true");
            formData.append('categories', $('#category').val());

            $.ajax({
                url: '../recipes/save_recipe',
                type: 'POST',
                contentType: false,
                processData: false,
                dataType: 'json',
                data: formData,
                success: function (response) {
                    if (response['result_code'] == 200) {
                        $('#saveRecipeMessage').css('display', 'none');
                        setTimeout('location="../recipes/recipe?id=" + response["id"];', 1000);
                    } else {
                        $('#saveRecipeMessage').text(response['error']);
                        $('#saveRecipeMessage').css('display', 'block');
                    }
                    $('.btn').removeAttr("disabled");
                }
            });
        } else {
            $('#saveRecipeMessage').text('Вес файла не должен превышать ' + fileSize + 'кб.');
            $('#saveRecipeMessage').css('display', 'block');
        }
    }
}


function deletePhoto() {
    $('.delete-photo-btn').attr("disabled", "true");
    let formData = new FormData();
    formData.append('recipes_id', $('#recipes_id').val());
    formData.append('file', $('#file').val());
    $.ajax({
        url: '../recipes/delete_photo',
        type: 'DELETE',
        contentType: false,
        processData: false,
        dataType: 'json',
        data: formData,
        success: function (response) {
            window.location.reload();
        }
    });
}