$(document).ready(function() {
    $("#miCarrusel").bxSlider({
        slideWidth: 0,
        adaptiveHeight: false,
        mode: 'fade',
        responsive: false,
        randomStart: true,
        keyboardEnabled: true,
        nextText: 'Sig.',
        prevText: 'Ant.',
        captions: true,
        auto: true,
        pause: 15000
    });
})