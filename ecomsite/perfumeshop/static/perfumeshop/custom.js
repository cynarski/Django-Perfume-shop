$(document).ready(function() {

    var cards = $('#perfume-container .row .card');
    console.log(cards);

    var maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());

    cards.height(maxHeight);
});
