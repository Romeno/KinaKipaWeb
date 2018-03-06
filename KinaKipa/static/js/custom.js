/**
 * Created by RomenoNB on 23.01.2018.
 */


/* * * * * Test AJAX script * * * * * */
//$(document).ready(function () {
//    $('body > header').click(function(event) {
//        console.log('clicked');
//
//        $.ajax( {
//            url: '/my_ajax',
//            method: 'POST',
//            data: '11',
//            complete: function(xhrRes, status) {
//                console.log(xhrRes, status);
//            }
//        });
//    });
//});


$('#id_q').change(function () {
    querry = $(this).val();
    console.log( querry );

    $.ajax({
        url: 'api/search/',
        data: {
            'q': querry
        },
        dataType: 'json',
        success: function (data) {
            if (data.films) {
                var names = '';
                for (var film in data.films) {
                    names += data.films[film]['name']
                }

                alert(names);
            }
        }
    });
});