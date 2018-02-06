ymaps.ready(init);
var myGeocoder = ymaps.geocode("минск");
myGeocoder.then(
    function (res) {
        map.geoObjects.add(res.geoObjects);
        // Выведем в консоль данные, полученные в результате геокодирования объекта.
        console.log(result.geoObjects.get(0).properties.get('metaDataProperty').getAll());
    },
    function (err) {
        // обработка ошибки
    }
);
//var myMap,
//    myPlacemark;
//
function init(){
//    myMap = new ymaps.Map("map", {
//        center: [53.9,27.56659],
//        zoom: 12
//    });
//
//    myPlacemark = new ymaps.Placemark([53.9,27.56659], {
//        hintContent: 'минск!',
//        balloonContent: 'Столица Беларусь'
//    });
//
//    myMap.geoObjects.add(myPlacemark);
//}
