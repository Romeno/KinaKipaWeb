ymaps.ready(init);
var myMap,
    myPlacemark;

function init(){
    myMap = new ymaps.Map("map", {
        center: [53.9,27.56659],
        zoom: 12
    });

    myPlacemark = new ymaps.Placemark([53.9,27.56659], {
        hintContent: 'Москва!',
        balloonContent: 'Столица России'
    });

    myMap.geoObjects.add(myPlacemark);
}