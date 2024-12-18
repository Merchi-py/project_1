$(".btn-price").click(function(){
    let btn = $(this)
        $.ajax("/", {
        "type": "POST",
        "async": true,
        "dataType": json,
        "data":{
            "price": btn.data("price")
        };
        "success": function(response){
        document.getElementById("#price-tours").innerhtml = `${response.picture}`
        document.getElementById("#price-tours").innerhtml = `${response.name}`
        document.getElementById("#price-tours").innerhtml = `${response.price}`
        document.getElementById("#price-tours").innerhtml = `${response.description}`
        document.getElementById("#price-tours").innerhtml = `${response.people}`
        document.getElementById("#price-tours").innerhtml = `${response.time}`
        }
    })
})