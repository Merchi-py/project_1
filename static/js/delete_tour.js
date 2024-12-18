$("#deleteTour").click(function(){
    var btn = $(this);
        $.ajax("/delete/tour/{id}", {
        "type": "POST",
        "async": true,
        "dataType": json,
        "data":{
        };
    })
})