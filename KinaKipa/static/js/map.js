ymaps.ready(init);
var kkMap;

function init(){
    kkMap = new ymaps.Map("map", {
        center: [53.9, 27.56], // Minsk coordinates
        zoom: 6
    });

    function addMovieScreening(screening) {
        ymaps.geocode(screening.location).then(
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

    $.ajax({
        url: '/ajax_put_events_on_map',
        method: 'GET',
        complete: function(xhrRes, status) {
            var events = xhrRes.responseJSON.events;

            for (var i = 0; i < events.length; i++) {
                addMovieScreening(events[i]);
            }
        }
    });

    // var marks = [{
    //     title: "Наўсікая з Даліны Вятроў",
    //     description: "Наўсікая з Даліны Вятроў на беларускай мове!",
    //     location: "Минск",
    //     start_date: "19:00 10 студзеня",
    //     end_date: "22:00 10 студзеня"
    // },];

    // myPlacemark = new ymaps.Placemark([53.9,27.56659], {
    //     hintContent: 'Москва!',
    //     balloonContent: 'Столица России'
    // });
    //
    // myMap.geoObjects.add(myPlacemark);
}