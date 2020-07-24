$(document).ready(function(){
    setInterval(updateinfo, 1000);

    function updateinfo(){
        var idcurrposition = Array.prototype.slice.call(document.querySelectorAll('.updatecurrposition')).map(function ( element ) {
            return element.id;
        });
        
        idcurrposition.forEach(element => {
            req = $.ajax({
                url : '/update',
                type : 'POST',
                data : {idval : element}
            });
    
            
            req.done(function(data){
                $('#'+element).text(data.result);
            });
    
        });
    };

});



$(document).ready(function(){

    $('.toggle').each(function(){
        $(this).click(function(){
//            var currdata = $(this).data('selected');
            var idval = $(this).attr('id');
            req = $.ajax({
                url: '/stoplossonoff',
                type: 'POST',
                data: {'idval': idval}
            });

//            req.done(function(data){
 //               $('#text'+element).text('success');
 //           });
        });
    });

});


$(document).ready(function(){
    setInterval(totalfunc, 5000)

    function totalfunc(){
        userval();
        currtotal();
        moreuserval();
    }


    function currtotal(){
        req = $.ajax({
            url : '/currtotal',
            type : 'POST',
            data : {idval : 0.0}
        });
        req.done(function(data){
//            $('.currtotalbalance').text(data.currtotalbalance);
            $('#grandxbtusd').text(data.result);
        });
    }


    function userval(){


        var currpositionids = Array.prototype.slice.call(document.querySelectorAll('.currposition')).map(function ( element ) {
            return element.id;
        });
        var actualpositionids = Array.prototype.slice.call(document.querySelectorAll('.actualposition')).map(function ( element ) {
            return element.id;
        });

        var longentrypriceids = Array.prototype.slice.call(document.querySelectorAll('.longentryprice')).map(function ( element ) {
            return element.id;
        });

        var shortentrypriceids = Array.prototype.slice.call(document.querySelectorAll('.shortentryprice')).map(function ( element ) {
            return element.id;
        });

        var entrypriceids = Array.prototype.slice.call(document.querySelectorAll('.entryprice')).map(function ( element ) {
            return element.id;
        });

        var liveprofitreturnids = Array.prototype.slice.call(document.querySelectorAll('.liveprofitreturn')).map(function ( element ) {
            return element.id;
        });

        var marginleverageids = Array.prototype.slice.call(document.querySelectorAll('.marginleverage')).map(function ( element ) {
            return element.id;
        });

        var bestrevenueids = Array.prototype.slice.call(document.querySelectorAll('.bestrevenue')).map(function ( element ) {
            return element.id;
        });

        currpositionids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val' : 'currposition', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });
        });

        actualpositionids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val' : 'actualposition', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });
        });

        longentrypriceids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val' : 'longentryprice', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });
        });

        shortentrypriceids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val' : 'shortentryprice', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });
        });
        entrypriceids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val' : 'entryprice', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });
        });

        liveprofitreturnids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val': 'profitreturn', 'idval': element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });

        });

        bestrevenueids.forEach(element => {
            req = $.ajax({
                url : '/userval',
                type : 'POST',
                data : {'val': 'bestrevenue', 'idval': element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            });

        });

        marginleverageids.forEach(element => {
            req = $.ajax({
                url : "/marginleverage",
                type : "POST",
                data : {'idval': element}
            });
            req.done(function(data){
                $('#'+element).text(data.result);
            })
        })

    }

    function moreuserval(){

        var currbalanceids = Array.prototype.slice.call(document.querySelectorAll('.currbalance')).map(function ( element ) {
            return element.id;
        });
        var positionamountids = Array.prototype.slice.call(document.querySelectorAll('.positionamount')).map(function ( element ) {
            return element.id;
        });
        var positionamountxbtids = Array.prototype.slice.call(document.querySelectorAll('.positionamountxbt')).map(function ( element ) {
            return element.id;
        });

        currbalanceids.forEach(element => {
            req = $.ajax({
                url : '/moreuserval',
                type : 'POST',
                data : {'val' : 'currbalance', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result)
            });
        });

        positionamountids.forEach(element => {
            req = $.ajax({
                url : '/moreuserval',
                type : 'POST',
                data : {'val' : 'positionamount', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result)
            });
        });

        positionamountxbtids.forEach(element => {
            req = $.ajax({
                url : '/moreuserval',
                type : 'POST',
                data : {'val' : 'positionamountxbt', 'idval' : element}
            });
            req.done(function(data){
                $('#'+element).text(data.result)
            });
        });






    }






});
