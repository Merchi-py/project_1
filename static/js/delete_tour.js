$(".deleteTour").click(function(event) {
    event.preventDefault();


    $.ajax("/delete_tour/" + $(this).closest('.block').find('.tourId').val(), {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "success": function(){}
    });
})