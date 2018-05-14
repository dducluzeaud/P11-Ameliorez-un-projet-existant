$('#new_email').on('submit', function(event){
                   event.preventDefault();
                   console.log("form submitted!")  // sanity check
                   new_email_post();
                   });

function new_email_post() {
    console.log("create post is working!") // sanity check
    var form = $('#new_email');
    var email_changed = $('#id_new_email').val();
    $.ajax({
           url: form.attr("action"),
           type: "POST",
           data: form.serialize(),
           // handle a successful response
           success : function(data) {
           if (data.form_is_valid) {
           alert("Adresse email modifié avec succès"); // remove the value from the input
           $("#new_email")[0].reset();
           $("#id_new_email").removeAttr("style");
           $('input[id=current_email]').val(email_changed);
           } else {
           alert("La nouvelle adresse email doit être différente")
           }
        },
    })
};

$('#new_passwd').on('submit', function(event){
                    event.preventDefault();
                    console.log("form submitted!")  // sanity check
                    new_passwd_post();
                    });

function new_passwd_post() {
    console.log("create post is working!") // sanity check
    var form = $('#new_passwd');
    $.ajax({
           url: form.attr("action"),
           type: "POST",
           data: form.serialize(),
           // handle a successful response
           success : function(data) {
           if (data.form_is_valid) {
           alert(data.msg); // remove the value from the input
           $("#new_passwd")[0].reset();
           } else {
           alert(data.msg)
           }
       },
   })
};
