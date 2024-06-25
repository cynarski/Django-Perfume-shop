$(document).ready(function() {

    var cards = $('#perfume-container .row .card');
    var maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());

    cards.height(maxHeight);
});


console.log("Working");

if(localStorage.getItem('cart')==null){
    var cart = {};
    console.log('ERROR');
}
else{
    cart = JSON.parse(localStorage.getItem('cart'));
}

$(document).on('click', '.atc', function(){
    console.log("Button clicked");
    var item_id = this.id.toString();
    console.log(item_id);
});
