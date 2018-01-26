/**
 * Created by RomenoNB on 23.01.2018.
 */


/* * * * * Test AJAX script * * * * * */
$(document).ready(function () {
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

/* * * * * *  Slick carousel slider * * * * * */
$(document).ready(function(){
    $('.carousel').slick({
      dots: true,
      slidesToShow: 1,
      infinite: true,
      fade: true,
      cssEase: 'linear',
      arrows: true,
      prevArrow: '<button type="button" class="slick-prev">Previous</button>',
      nextArrow: '<button type="button" class="slick-next">Next</button>',
      dotsClass: 'slick-dots kinakipa-slick-dots',
      autoplay: true,
      autoplaySpeed: 6000,
    });
});