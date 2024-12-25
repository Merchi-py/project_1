$("#openBasket").click(function(){
    let btn = $(this)
    $('#book').data('url', btn.data('url'));

    $("#book").click(function(){
        $.ajax("/buy", {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "data": {},
        "success": function(response){
        if (message){
            var message = response.message
        const basketModal = new bootstrap.Modal("#basketModal")
        basketModal.hide();
        }
        }
        })
    }
)
});

