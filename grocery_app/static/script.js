$(document).ready(function(){

    $('#update_account').submit(function(e){
        e.preventDefault()
        $.ajax({
            url: '/noorani/account/update', 
            method: 'post',
            data: $(this).serialize(),
            success: function(serverResponse){
                console.log("HAH!")

            }

            })
        })
    })

