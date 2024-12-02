$(".add_tour").click(function(){
    let btn = $(this)
    $("#saveTour").data("url", btn.data("url"))
});

$("#saveTour").click(function(){
    $.ajax("btn.data("url")", {
    'type': 'POST',
       'async': true,
       'dataType': 'json',
       'data': {
            "name": $("#Name_Tour").val()
            "price": $("#Price").val()
            "description": $("#Description").val()
            "time": $("#Time").val()
            "people": $("#People").val()
       },
       "success": function(response){
       const add_tourModal = new bootstrap.Modal("#add_tourModal")
            add_tourModal.hide();
       }
    })
})
