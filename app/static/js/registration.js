$('.reg').click(function (){
    let btn = $(this);
    $('#saveRegistration').data('url', btn.data('url'));
});

$('#saveRegistration').click(function (){
    let btn = $(this);
   $.ajax(btn.data('url'), {
       'type': 'POST',
       'async': true,
       'dataType': 'json',
       'data': {
            "name": $("#Name").val(),
            "email": $("#Email").val(),
            "password": $("#Password").val(),
            "r_password": $("#RPassword").val()
       },
       'success': function (response){
            const registrationModal = new bootstrap.Modal("#registrationModal")
            registrationModal.hide();
       }
   })
});
