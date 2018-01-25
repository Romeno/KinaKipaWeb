/**
 * Created by RomenoNB on 23.01.2018.
 */



$().ready(function () {
    $('body > header').click(function(event) {
        console.log('clicked');

        $.ajax( {
            url: '/my_ajax',
            method: 'POST',
            data: '11',
            complete: function(xhrRes, status) {
                console.log(xhrRes, status);
            }
        });
    });
});
