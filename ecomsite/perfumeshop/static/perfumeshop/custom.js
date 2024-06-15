$(document).ready(function() {
    // Znajdź wszystkie karty w sekcji z identyfikatorem perfume-container
    var cards = $('#perfume-container .row .card');
    console.log(cards);
    
    // Znajdź najwyższą wysokość karty
    var maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());
    
    // Ustaw równą wysokość dla wszystkich kart
    cards.height(maxHeight);
});
