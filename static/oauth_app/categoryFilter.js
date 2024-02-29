function filterByCategory(category) {
    // Your function implementation
    $('#cuisine_type').val(category);
    $('#restaurant-filter-form').submit();
    window.location.href = '/map/';
}