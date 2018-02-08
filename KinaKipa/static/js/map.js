ymaps.ready(init);
var kkMap;

function init(){
    kkMap = new ymaps.Map("map", {
        center: [53.9, 27.56], // Minsk coordinates
        zoom: 6
    });

    function createScreeningPlacemark(screening) {
        return ymaps.geocode(screening.location).then(
            function (res) {
                var coords = res.geoObjects.get(0).geometry.getCoordinates();
                var placemark = new ymaps.Placemark(coords, {
                    hintContent: screening.title,
                    balloonContentHeader: screening.title,
                    balloonContentBody: screening.balloon_description,
                });

                // kkMap.geoObjects.add(placemark);
                // kkMap.geoObjects.add(res.geoObjects);
                // // Выведем в консоль данные, полученные в результате геокодирования объекта.
                // console.log(res.geoObjects.get(0).properties.get('metaDataProperty').getAll());

                return [placemark, coords];
            },
            function (err) {
                console.error("Error loading data for screening", screening, err);
            }
        );
    }

    $.ajax({
        url: '/api/events',
        method: 'GET',
        complete: function(xhrRes, status) {
            var events = xhrRes.responseJSON.events;

            var promises = [];
            for (var i = 0; i < events.length; i++) {
                promises.push(createScreeningPlacemark(events[i]));
            }

            Promise.all(promises).then(function(placemarksAndCoords) {
                var myGeoObjects = new ymaps.GeoObjectCollection({}, {
                    // preset: "islands#redCircleIcon",
                    // strokeWidth: 4,
                    // geodesic: true
                });

                for (var i = 0; i < placemarksAndCoords.length; i++) {
                    myGeoObjects.add(placemarksAndCoords[i][0]);
                }

                // Добавляем коллекцию на карту.
                kkMap.geoObjects.add(myGeoObjects);

                // ymaps.getZoomRange('yandex#map', placemarksAndCoords[0][1]).then(function (zoomRange) {
                //     kkMap.setZoom(zoomRange[1]-2);
                // });

                // Устанавливаем карте центр и масштаб так, чтобы охватить коллекцию целиком.
                kkMap.setBounds(myGeoObjects.getBounds(), {'checkZoomRange': true});
            });
        }
    });

    // var events = {"events": [{
    //         title: "Наўсікая з Даліны Вятроў",
    //         description: "Наўсікая з Даліны Вятроў на беларускай мове!",
    //         location: "Минск, Фабрициуса, 4",
    //         start_date: "19:00 10 студзеня",
    //         end_date: "22:00 10 студзеня"
    //     },
    //     {
    //         title: "Хадзячы Замак Хаула",
    //         description: "Хадзячы Замак Хаула на беларускай мове!",
    //         location: "Минск, пр. Победителей, 47/1",
    //         start_date: "19:00 12 студзеня",
    //         end_date: "22:00 12 студзеня"
    //     }
    // ]};
    //
    // for (var i = 0; i < events.events.length; i++) {
    //     addMovieScreening(events.events[i]);
    // }
}