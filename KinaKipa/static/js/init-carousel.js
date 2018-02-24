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