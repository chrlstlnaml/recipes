function searchRecipes(page) {
    let myForms = $('#searchRecipesForm');
    let formData = new FormData(myForms[0]);
    formData.append('ingredients', $('#ingredients').val());
    formData.append('categories', $('#categories').val());
    formData.append('complexity', $('#complexity').val());
    formData.append('page', page);

    $.ajax({
        url: '../recipes/search_for_recipes',
        type: 'POST',
        contentType: false,
        processData: false,
        dataType: 'json',
        data: formData,
        success: function (response) {
            $('#recipesList').html(response);
        }
    });
}