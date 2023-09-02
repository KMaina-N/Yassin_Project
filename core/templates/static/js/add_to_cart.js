// add to cart
const addToCartBtn = document.querySelector('.product_add_to_cart a');

// addtocartbtn data-product-id
const productId = addToCartBtn.dataset.productId;
addToCartBtn.addEventListener('click', function () {
    // ajax request
    var url = "/add_to_cart/";
    var data = {
        'id': productId,
        'quantity': input,
    }
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            // update the cart amount
            // document.querySelector('.cart .amt').innerHTML = input;
        }
    })

    // update quantity in cart
    var cart_quantity_url = "/quantity_in_cart/";
    // sleep(2 seconds)
    setTimeout(function () {
        $.ajax({
            url: cart_quantity_url,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                document.querySelector('.cart span .amt').innerHTML = data.quantity;
            }
        });
    }, 2000); // 2000 milliseconds (2 seconds)

})