$(document).on('click', ".add-to-cart", function () {
    debugger
    var _vm = $(this);
    var _index = _vm.attr('id');
    $("#"+_index).hide();
	// $(".submitWidget"+ _index).show();
    $('.submitWidget-' + _index).css("display", "block");
    var _qty = $("#product-qty-" + _index).val();
    var _productid = $(".product_id-" + _index).val();
    var _productImage = $(".product-image-" + _index).val();
    var _title = $(".meta_title-" + _index).val();
    var _price = $(".product-price-" + _index).text();
    $.ajax({
        url: '/mycart',
        data: {
            'id': _productid,
            'image': _productImage,
            'qty': _qty,
            'title': _title,
            'price': _price
        },
        dataType: 'json',
        beforeSend: function () {
            _vm.attr('disabled', true);
        },
        success: function (res) {
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
        }
    });
});