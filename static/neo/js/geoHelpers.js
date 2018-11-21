function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(callbackGetLocation);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

function callbackGetLocation(position) {
    return [
        position.latitude,
        position.longitude
    ];
}