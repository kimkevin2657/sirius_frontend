$(document).ready(function(){

    $('.toggle').each(function(){
        $(this).click(function(){
//            var currdata = $(this).data('selected');
            var idval = $(this).attr('id');
            req = $.ajax({
                url: '/botonoff',
                type: 'POST',
                data: {'idval': idval}
            });

//            req.done(function(data){
//               $('#text'+element).text('success');
//            });
        });
    });

});