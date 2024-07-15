$(document).ready(function() {
    var cards = $('#perfume-container .row .card');
    var maxHeight = Math.max.apply(null, cards.map(function () {
        return $(this).height();
    }).get());
    cards.height(maxHeight);

    if (localStorage.getItem('cart') == null) {
        var cart = {};
        console.log('ERROR');
    } else {
        var cart = JSON.parse(localStorage.getItem('cart'));
        DisplayCart(cart);
    }

    $(document).on('click', '.atc', function() {
        var item_id = this.id.toString();
        console.log(item_id);

        if (cart[item_id] != undefined) {
            cart[item_id] += 1;
        } else {
            cart[item_id] = 1;
        }
        console.log(cart);
        localStorage.setItem('cart', JSON.stringify(cart));
        document.getElementById('cart').innerHTML = "Cart(" + Object.keys(cart).length + ")";
        DisplayCart(cart);
    });

    $('[data-toggle="popover"]').popover();
});

function DisplayCart(cart) {
    var cartString = "<h5>Your cart</h5>";
    var cartIndex = 1;

    for (var x in cart) {
        if (cart.hasOwnProperty(x)) {
            cartString += cartIndex + ". ";

            var itemElement = document.getElementById("nm" + x);

            if (itemElement) {
                cartString += itemElement.innerHTML + " Qty: " + cart[x] + "</br>";
            } else {
                console.error('Element o id "nm' + x + '" nie istnieje w DOM');
                cartString += "Unknown Item (id: nm" + x + ") Qty: " + cart[x] + "</br>";
            }

            cartIndex += 1;
        }
    }

    cartString += "<a href=\"/checkout\" class=\"btn btn-warning mt-2\">Checkout</a>\n";

    var cartElement = document.getElementById("cart");
    if (cartElement) {
        cartElement.setAttribute('data-content', cartString);

        $(cartElement).popover('dispose');
        $(cartElement).popover();
    } else {
        console.error('Element o id "cart" nie istnieje w DOM');
    }
}