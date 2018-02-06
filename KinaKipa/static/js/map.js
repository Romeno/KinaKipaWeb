ymaps.ready(init);
var kkMap;

function init(){
    kkMap = new ymaps.Map("map", {
        center: [53.9, 27.56], // Minsk coordinates
        zoom: 6
    });

    var marks = [{
        title: "Наўсікая з Даліны Вятроў",
        description: "Наўсікая з Даліны Вятроў на беларускай мове!",
        location: "Минск",
        start_date: "19:00 10 студзеня",
        end_date: "22:00 10 студзеня"
    },];

    function addMovieScreening(screening) {
        ymaps.geocode("Минск").then(
            function (res) {
                var placemark = new ymaps.Placemark(res.geoObjects.get(0).geometry.getCoordinates(), {
                    hintContent: screening.title,
                    balloonContent: screening.description
                });

                kkMap.geoObjects.add(placemark);
                // kkMap.geoObjects.add(res.geoObjects);
                // // Выведем в консоль данные, полученные в результате геокодирования объекта.
                // console.log(res.geoObjects.get(0).properties.get('metaDataProperty').getAll());
            },
            function (err) {
                console.error("Error loading data for screening", screening, err);
            }
        );
    }

    for (var i = 0; i < marks.length; i++) {
        addMovieScreening(marks[i]);
    }

    // myPlacemark = new ymaps.Placemark([53.9,27.56659], {
    //     hintContent: 'Москва!',
    //     balloonContent: 'Столица России'
    // });
    //
    // myMap.geoObjects.add(myPlacemark);
}