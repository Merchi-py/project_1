$(".add_to_basket").click(function(){
    var btn = $(this);
        $.ajax(btn.data("url"), {
        "type": "POST",
        "async": true,
        "dataType": "json",
        "data": {
        }
    });
})