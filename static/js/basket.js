$("#openBasket").click(function(){
    var btn = $(this);
        $.ajax(btn.data("url"), {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "data": {
        },
        "success": function(response){
        document.getElementById("bask").innerHTML = response.basket
        }
    });
})