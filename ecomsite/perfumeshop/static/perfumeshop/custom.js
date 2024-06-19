$(document).ready(function() {

    var cards = $('#perfume-container .row .card');
    console.log(cards);
    
    var maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());
    
    cards.height(maxHeight);
});

document.getElementById('minPrice').addEventListener('input', function() {
    document.getElementById('price-filter-form').submit();
});

document.getElementById('maxPrice').addEventListener('input', function() {
    document.getElementById('price-filter-form').submit();
});


