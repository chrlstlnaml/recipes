function searchRecipes() {
    let formData = new FormData();
    formData.append('ingredients', $('#ingredients').val());

    $.ajax({
        url: '../recipes/search_for_recipes',
        type: 'POST',
        contentType: false,
        processData: false,
        dataType: 'json',
        data: formData,
        success: function (response) {
            alert(response);
        }
    });
}