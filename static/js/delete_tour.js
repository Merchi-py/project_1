$(".deleteTour").click(function(event) {
    event.preventDefault();
    let a = $(this)


    $.ajax("/delete_tour/" + a.closest('.block').find('.tourId').val(), {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "success": function(response){
        console.log(a.closest('.block'))
        a.closest('.block').remove()
        }
    });
})