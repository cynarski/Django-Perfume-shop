$(document).ready(function() {

    let cards = $('#perfume-container .row .card');

    let maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());

    cards.height(maxHeight);
});
