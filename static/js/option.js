$(".btn-price").click(function(){
    let btn = $(this)
        $.ajax("/", {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "data":{
            "price": btn.data("price")
        },
        "success": function(response){
        document.getElementById("price-tours").innerHTML = response.tours

        }
    });
})