$(document).ready(function() {

    mapboxgl.accessToken = 'pk.eyJ1IjoicmVwdXRnbG9yeTEiLCJhIjoiY2t2aDJ4c3JtMWo4NDJ2cTV2eWduc3YyZiJ9.rP6dQnOF2j00N134I0zpvg';
    const mymap = new mapboxgl.Map({
        container: 'map', // container ID
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [28, 37], // starting position [lng, lat]
        zoom: 3 // starting zoom
    });

    mymap.doubleClickZoom.disable();

    function print_all_routes() {
        var res;
        $.ajax({
            url: "http://127.0.0.1:5000/?xleft=33&xright=41&yleft=20&yright=26",
            crossDomain: true,
            method: "GET",
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data) {
                for (let i = 0; i < data.length; i++) {

                    const popup = new mapboxgl.Popup()
                        .setLngLat([data[i]["y"], data[i]["x"]])
                        .setHTML(data[i]["data"])
                        .addTo(mymap);

                    new mapboxgl.Marker().setLngLat([data[i]["y"], data[i]["x"]]).setPopup(popup).addTo(mymap);
                }
            }
        });
    }

    print_all_routes();

});
