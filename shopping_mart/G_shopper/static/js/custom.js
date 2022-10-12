$(document).ready(function(){
    $('.submitWidget').css("display", "none");
    $('.remove').css("display","none")
});

//add to cart increment and decrement
function incrementValue(prod_id) {
    var value = parseInt(document.getElementById('product-qty-' + prod_id).value, 10);
    value = isNaN(value) ? 0 : value;
    if (value < 10) {
        value++;
        document.getElementById('product-qty-' + prod_id).value = value;
        $.ajax({
        url: '/updatecart',
        data: {
            'id': prod_id,
            'qty': value,
        },
        dataType: 'json',
        success: function (res) {
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
        }
    });
    }
}

function decrementValue(prod_id) {
    var value = parseInt(document.getElementById('product-qty-' + prod_id).value, 10);
    value = isNaN(value) ? 0 : value;
    if (value >= 1) {
        value--;
        document.getElementById('product-qty-' + prod_id).value = value;
        if (value == 0) {
            $('.submitWidget-'+prod_id).css("display", "none");
            $("#"+prod_id).show();


            $.ajax({
            url: '/deletefromcart',
            data: {
                'id': prod_id,

            },
            dataType: 'json',
            success: function (res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
            }
    });
        }

    }

}




//add ro cart

$(document).on('click', ".add-to-cart", function () {
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
    console.log(_qty, _productid, _title);

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


// addwishlist

$(document).on('click',".add-wishlist",function(){
    
    var _pid=$(this).attr('data-product');
    var _vm=$(this);
    
    $.ajax({
        
        url:"/add-wishlist",
        data:{
            product:_pid
        },
        dataType:'json',
        success:function(res){
            if(res.bool==true){
                _vm.addClass('disabled').removeClass('add-wishlist');
            }
        }
    });
});


$(document).on('click', ".apply", function () {
    var coupon = $("#coupons").val();
    console.log(coupon);
    $.ajax({
        type: "GET",
        url: '/coupon',
        data: {
            'cart_coupon': coupon,
        },
        
        dataType: 'json',
        success: function (data) {
            $("#apply").hide();
            $('#remove').css("display", "block");
            var total_amt = document.getElementById('prd_amt').innerText;
            var dist_amt = 100 * (total_amt-data[0])/(total_amt) ;
            var final_amt = (total_amt-dist_amt)
            document.getElementById('ftotal').innerHTML= final_amt;
          
        }
    });
});
