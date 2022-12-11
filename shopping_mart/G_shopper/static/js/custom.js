$(document).ready(function(){
    $('.submitWidget').css("display", "none");
    $('.remove').css("display","none")

    // $.ajax({
    //     method: 'GET',
    //     url: '/home',
    //     data: {
            
    //     },
    //     dataType: 'json',
    //     success: function (res) {
            
    //     }
    // });
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
            document.getElementById("coupons").disabled = true;
            $('#remove').css("display", "block");
            var total_amt = document.getElementById('prd_amt').innerText;
            var dist_amt = (total_amt * data['percent_off'])/100 ;
            if (total_amt < 500) {
                total_amt = total_amt + 50  
            }
            else {
                total_amt
            }
            var final_amt = (total_amt-dist_amt)
            var final_amt = Math.round(final_amt).toFixed(2)
            document.getElementById('ftotal').innerHTML= final_amt;
            document.getElementById('msg').innerHTML= data['percent_off'] + "% applied";
        }
    });
});

$(document).on('click', ".remove", function () {
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
            $("#remove").hide();
            $('#apply').css("display", "block");
            document.getElementById("coupons").disabled = false;
            var total_amt = document.getElementById('prd_amt').innerText;          
            var final_amt = total_amt
            document.getElementById('ftotal').innerHTML= final_amt;
            // document.getElementById('dist').innerHTML= data;
            document.getElementById('msg').innerHTML= "";

        }
    });
});


function handleSubmit () {
    const ftotal = document.getElementById('ftotal').innerText;  
    sessionStorage.setItem("TOTAL", ftotal);
    const ship_amount = document.getElementsByClassName('shipamt').innerText;
    sessionStorage.setItem('ship_amt',ship_amount)
    return;
}


$(document).on('click',".categorie",function(){
    var _vm = $(this);
    var _index = _vm.attr('id');
    let option = document.getElementById('sl2').value;
    let value = option.split(",");
    let min_price = value[0];
    let max_price = value[1];
    console.log(min_price)
    console.log(max_price)
    console.log(_index)
    // var category = document.getElementsByClassName('categories_'+ _index);
    // console.log(category) 
    $.ajax({
        method:'GET',
        url:"/category",
        data: {"category_id":_index,
                "min_price":min_price,
                "max_price":max_price
                },
        dataType: "json",
        success:function(data){
            var image = (data.product_img[0].image_path)
            var url = "/media/".concat(image)
            console.log(data.product.length)
            $ .each(data,function(){
            $('#cart_data').html(  
                ` <div class="col-sm-4" >
                            <div class="product-image-wrapper">
                                <div class="single-products">
                                    <div class="productinfo text-center">
                                        <img src="`+url+`" alt="" />
                                        <p>`+data.product[0].name+`</p>
                                        <input type="hidden" class="product-image-{{prod.id}}"
                                            value="{{prod.productimages_set.first.image_path.url}"/>
                                        <th>$ <span class="product-price-{{prod.id}}">`+data.product[0].price+`</span></th>
                                        <input type="hidden" class="product_id-{{prod.id}}" value="{{prod.id}}">
                                        <input type="hidden" class="meta_title-{{prod.id}}" value="{{prod.meta_title}}">
                                        <br>
                                    <button class="btn btn-default add-to-cart" id="{{prod.id}}"><i
                                        class="fa fa-shopping-cart addcart"></i>Add to cart</button>

                            <div class="cart_quantity_button submitWidget submitWidget-{{prod.id}}">
                        <input type="button" onclick="decrementValue('{{prod.id}}')" value=" - " />
                        <input type="text" id="product-qty-{{prod.id}}" name="quantity" value="1"
                                                maxlength="2" max="10" size="1" readonly />
                        <input type="button" onclick="incrementValue('{{prod.id}}')" value="+" />
                                        </div> <br>
                        <div class="choose"><ul class="nav nav-pills nav-justified">
                                                
                            <li><a href="{% url 'G_shopper:product_detail' prod.id %}" value=""><i class="fa fa-plus-square"></i>view product</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div> `
            );  
        });           
        }
    });
});


  

$(document).on('click',".slider-track",function(){
    // var category = document.getElementsByClassName('categories_')
    // console.log(category)
    let option = document.getElementById('sl2').value;
    let value = option.split(",");
    let min_price = value[0];
    let max_price = value[1];
    console.log(min_price)
    console.log(max_price)
    $.ajax({
        method:'GET',   
        url:"/price",
        data: {
            "min_price":min_price,
            "max_price":max_price,},
        dataType: "json",
        success:function(data){
            console.log(data)
            console.log(data.product[0][1])
            console.log(data.product[1][0])
            console.log(data.product[2][0])
            
            debugger;
            $("#cart_data").empty();
            for (let i = 0; i < data.product[0].length; i++){
                var image = (data.product[2][i])
                var url = "/media/".concat(image)
             { let item_content = '<div class="col-sm-4" ><div class="product-image-wrapper"> <div class="single-products"><div class="productinfo text-center"><img src="'+url+'" alt="" /><p>'+data.product[0][i]+'</p><input type="hidden" class="product-image-{{prod.id}}"value="{{prod.productimages_set.first.image_path.url}"/><th>$ <span class="product-price-{{prod.id}}">'+data.product[1][i]+'</span></th><input type="hidden" class="product_id-{{prod.id}}" value="{{prod.id}}"><input type="hidden" class="meta_title-{{prod.id}}" value="{{prod.meta_title}}"><br><button class="btn btn-default add-to-cart" id="{{prod.id}}"><i class="fa fa-shopping-cart addcart"></i>Add to cart</button><div class="cart_quantity_button submitWidget submitWidget-{{prod.id}}"><input type="button" onclick="decrementValue(" value=" - " /><input type="text" id="product-qty-{{prod.id}}" name="quantity" value="1"maxlength="2" max="10" size="1" readonly /><input type="button" onclick="incrementValue()" value="+" /></div> <br><div class="choose"><ul class="nav nav-pills nav-justified"><li><a href="{% url  prod.id %}" value=""><i class="fa fa-plus-square"></i>view product</a></li></ul></div></div></div></div></div>'
            $("#cart_data").append(item_content);
            }   
        }
        }
    });
                                                
});


        





