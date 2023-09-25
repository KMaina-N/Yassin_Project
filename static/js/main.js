// Select all elements with the class '.product_add_to_cart a'
console.log('Update some code')
const addToCartBtns = document.querySelectorAll('.product_add_to_cart a');
var input = 1
// Define your common functionality
function addToCart(productId) {
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
            // Update the cart amount
            // document.querySelector('.cart .amt').innerHTML = input;
        }
    })

    // Update quantity in cart
    var cart_quantity_url = "/quantity_in_cart/";
    // Sleep (2 seconds)
    setTimeout(function () {
        $.ajax({
            url: cart_quantity_url,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                // Update the cart amount which is stored in the value attribute of the i element
                // document.querySelector('.cart span .amt').

                // document.querySelector('.cart span .amt').innerHTML = data.quantity;
                document.querySelector('.cart span .amt').setAttribute('value', data.quantity);
            }
        });
    }, 1000); // 2000 milliseconds (2 seconds)
}

// Add event listeners to each element
addToCartBtns.forEach(function (addToCartBtn) {
    addToCartBtn.addEventListener('click', function () {
        // Get the 'data-product-id' attribute from the clicked element
        const productId = addToCartBtn.dataset.productId;
        addToCart(productId);
    });
});
