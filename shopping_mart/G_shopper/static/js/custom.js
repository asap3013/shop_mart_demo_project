$(document).ready(function () {
  $(".submitWidget").css("display", "none");
  $(".remove").css("display", "none");

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

$(document).ready(function() {
setTimeout(function() {
  $('#success-alert').fadeOut('fast');
}, 1000);
});

$(document).ready(function() {
setTimeout(function() {
  $('#error-alert').fadeOut('fast');
}, 1000);
});



//add to cart increment and decrement
function incrementValue(product_id) {
  debugger;
  var value = parseInt(
    document.getElementById("product-qty-" + product_id).value,
    10
  );
  value = isNaN(value) ? 0 : value;
  if (value < 50) {
    value++;
    document.getElementById("product-qty-" + product_id).value = value;
    $.ajax({
      url: "/updatecart",
      data: {
        id: product_id,
        qty: value,
      },
      dataType: "json",
      success: function (data) {
        a = data
        console.log(a)
        $.each(data, function () {
          $(".price").empty()
          {
            let item_content = '<td id="price">'+ 'Rs '+ a['data']['total_amt'] +'</td>'
            $(".price").append(item_content)
          }
        })
    
      },
    });
  }
}

function decrementValue(product_id) {
  debugger;
  var value = parseInt(
    document.getElementById("product-qty-" + product_id).value,
    10
  );
  value = isNaN(value) ? 0 : value;
  if (value >= 1) {
    value--;
    document.getElementById("product-qty-" + product_id).value = value;
    // if (value == 1) {
      // $(".submitWidget-" + product_id).css("display", "none");
      // $("#" + product_id).show();

      $.ajax({
        url: "/deletefromcart",
        data: {
          id: product_id,
          qty: value
        },
        dataType: "json",
        success: function (data) {
          a = data
          $.each(data, function () {
            $(".price").empty()
            {
              let item_content = '<td id="price">'+ 'Rs '+ a['data']['total_amt'] +'</td>'
              $(".price").append(item_content)
            }
          })
        },
      });
    }
  }
// }

//add ro cart

$(document).on("click", ".add-to-cart", function () {
  debugger;
  var _vm = $(this);
  var _index = _vm.attr("id");
  // $("#" + _index).hide();
  // $(".submitWidget"+ _index).show();
  // $(".submitWidget-" + _index).css("display", "block");
  var _qty = $("#product-qty-" + _index).val();
  var _productid = $(".product_id-" + _index).val();
  var _productImage = $(".product-image-" + _index).val();
  var _title = $(".meta_title-" + _index).val();
  var _price = $(".product-price-" + _index).text();
  $.ajax({
    url: "/mycart",
    data: {
      id: _productid,
      image: _productImage,
      qty: _qty,
      title: _title,
      price: _price,
    },
    dataType: "json",
    beforeSend: function () {
      _vm.attr("disabled", true);
    },
    success: function (res) {
      $(".cart-list").text(res.totalitems);
      _vm.attr("disabled", false);
    },
  });
});

// addwishlist

$(document).on("click", ".add-wishlist", function () {
  debugger;
  var _pid = $(this).attr("data-product");
  var _vm = $(this);

  $.ajax({
    url: "/add-wishlist",
    data: {
      product: _pid,
    },
    dataType: "json",
    success: function (res) {
      if (res.bool == true) {
        _vm.addClass("disabled").removeClass("add-wishlist");
        // $(".add-wishlist").css("display", "block");

      }
    },
  });
});

$(document).on("click", ".apply", function () {
  var coupon = $("#coupons").val();
  console.log(coupon);
  $.ajax({
    type: "GET",
    url: "/coupon",
    data: {
      cart_coupon: coupon,
    },
    dataType: "json",
    success: function (data) {
      debugger;
      $("#apply").hide();
      document.getElementById("coupons").disabled = true;
      $("#remove").css("display", "block");
      var total_amt = document.getElementById("prd_amt").innerText;
      var dist_amt = (total_amt * data["percent_off"]) / 100;
      if (total_amt < 500) {
        total_amt = total_amt + 50;
      } else {
        total_amt;
      }
      var final_amt = total_amt - dist_amt;
      var final_amt = Math.round(final_amt).toFixed(2);
      document.getElementById("ftotal").innerHTML = final_amt;
      document.getElementById("msg").innerHTML =
        'Rs'+ dist_amt + " Saved   ";
    },
  });
});

$(document).on("click", ".remove", function () {
  var coupon = $("#coupons").val();
  console.log(coupon);
  $.ajax({
    type: "GET",
    url: "/coupon",
    data: {
      cart_coupon: coupon,
    },
    dataType: "json",
    success: function (data) {
      $("#remove").hide();
      $("#apply").css("display", "block");
      document.getElementById("coupons").disabled = false;
      var total_amt = document.getElementById("prd_amt").innerText;
      var final_amt = total_amt;
      document.getElementById("ftotal").innerHTML = final_amt;
      // document.getElementById('dist').innerHTML= data;
      document.getElementById("msg").innerHTML = "";
    },
  });
});

function handleSubmit() {
  const ftotal = document.getElementById("ftotal").innerText;
  sessionStorage.setItem("TOTAL", ftotal);
  const ship_amount = document.getElementsByClassName("shipamt").innerText;
  sessionStorage.setItem("ship_amt", ship_amount);
  return;
}

$('.categorie').on("click",function(){
  $(this).addClass("active");
  $(".active").attr('id')   
  var _vm = $(this);
  var _index = _vm.attr("id");
  $('#catagory_id').val(_index)
})

$('.slider-track').on("change",function(){
  
})


$('.categorie').add('.slider-track').on("click", function () {
  debugger;
  $(this).addClass("active");
  $(".active").attr('id')   
  var _vm = $(this);
  var _index = _vm.attr("id");
  console.log(_index)
  if(_index == undefined){
    _index = $('#catagory_id').val()
  }
  var option = document.getElementById("sl2").value;
  var value = option.split(",");
  var min_price = value[0];
  var max_price = value[1];
  console.log(min_price);
  console.log(max_price);
  console.log(min_price);
  console.log(max_price);
  console.log(_index);
  $.ajax({
    method: "GET",
    url: "/price",
    data: { category_id: _index, min_price: min_price, max_price: max_price },
    dataType: "json",
    success: function (data) {
      debugger;
      $(this).addClass("active");
      console.log(data.product.length);
      if (data.cat ==  0) {
        $.each(data, function () {
        var image = data.product_img[0].image_path;
        var url = "/media/".concat(image);
          $("#cart_data").html(
            ` <div class="col-sm-4" >
                            <div class="product-image-wrapper">
                                <div class="single-products">
                                    <div class="productinfo text-center">
                                        <img src="` +
              url +
              `" alt="" />
                                        <p>` +
              data.product[0].name +
              `</p>
                                        <input type="hidden" class="product-image-{{prod.id}}"
                                            value="{{prod.productimages_set.first.image_path.url}"/>
                                        <th>$ <span class="product-price-{{prod.id}}">` +
              data.product[0].price +
              `</span></th>
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
      else if (data.cat == 1) {
        debugger;
                $("#cart_data").empty();
                for (let i = 0; i < data.product[0].length; i++) {
                  var image = data.product[2][i];
                  var url = "/media/".concat(image);
                  {
                    let item_content =
                      '<div class="col-sm-4" ><div class="product-image-wrapper"> <div class="single-products"><div class="productinfo text-center"><img src="' +
                      url +
                      '" alt="" /><p>' +
                      data.product[0][i] +
                      '</p><input type="hidden" class="product-image-{{prod.id}}"value="{{prod.productimages_set.first.image_path.url}"/><th>$ <span class="product-price-{{prod.id}}">' +
                      data.product[1][i] +
                      '</span></th><input type="hidden" class="product_id-{{prod.id}}" value="{{prod.id}}"><input type="hidden" class="meta_title-{{prod.id}}" value="{{prod.meta_title}}"><br><button class="btn btn-default add-to-cart" id="{{prod.id}}"><i class="fa fa-shopping-cart addcart"></i>Add to cart</button><div class="cart_quantity_button submitWidget submitWidget-{{prod.id}}"><input type="button" onclick="decrementValue(" value=" - " /><input type="text" id="product-qty-{{prod.id}}" name="quantity" value="1"maxlength="2" max="10" size="1" readonly /><input type="button" onclick="incrementValue()" value="+" /></div> <br><div class="choose"><ul class="nav nav-pills nav-justified"><li><a href="{% url  prod.id %}" value=""><i class="fa fa-plus-square"></i>view product</a></li></ul></div></div></div></div></div>';
                    $("#cart_data").append(item_content);
                  }
                }
              } 
      else {
        $.each(data, function () {
          $("#cart_data").html(
            ` <div class="col-sm-4" >
                            <div class="product-image-wrapper">
                                <div class="single-products">
                                    <div class="productinfo text-center">
                                        <img src="+url+" alt="" />
                                        <p>` +
              "Product not available" +
              `</p>
                                        <input type="hidden" class="product-image-{{prod.id}}"
                                            value="{{prod.productimages_set.first.image_path.url}"/>
                                        <th>$ <span class="product-price-{{prod.id}}">+data.product[0].price+</span></th>
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
    },
  });
});


// $(document).on("click", ".slider-track", function () {
//   // var category = document.getElementsByClassName('categories_')
//   // console.log(category)
//   debugger;
//   let option = document.getElementById("sl2").value;
//   let value = option.split(",");
//   let category = sessionStorage.getItem("category");
//   let min_price = value[0];
//   let max_price = value[1];
//   console.log(min_price);
//   console.log(max_price);
//   $.ajax({
//     method: "GET",
//     url: "/price",
//     data: {
//       category: category,
//       min_price: min_price,
//       max_price: max_price,
//     },
//     dataType: "json",
//     success: function (data) {
//       console.log(data);
//       debugger;
//       // console.log(data.product[0][1])
//       // console.log(data.product[1][0])
//       // console.log(data.product[2][0])
//     //   if (data.product.length.length > 3) {
//         $("#cart_data").empty();
//         for (let i = 0; i < data.product[0].length; i++) {
//           var image = data.product[2][i];
//           var url = "/media/".concat(image);
//           {
//             let item_content =
//               '<div class="col-sm-4" ><div class="product-image-wrapper"> <div class="single-products"><div class="productinfo text-center"><img src="' +
//               url +
//               '" alt="" /><p>' +
//               data.product[0][i] +
//               '</p><input type="hidden" class="product-image-{{prod.id}}"value="{{prod.productimages_set.first.image_path.url}"/><th>$ <span class="product-price-{{prod.id}}">' +
//               data.product[1][i] +
//               '</span></th><input type="hidden" class="product_id-{{prod.id}}" value="{{prod.id}}"><input type="hidden" class="meta_title-{{prod.id}}" value="{{prod.meta_title}}"><br><button class="btn btn-default add-to-cart" id="{{prod.id}}"><i class="fa fa-shopping-cart addcart"></i>Add to cart</button><div class="cart_quantity_button submitWidget submitWidget-{{prod.id}}"><input type="button" onclick="decrementValue(" value=" - " /><input type="text" id="product-qty-{{prod.id}}" name="quantity" value="1"maxlength="2" max="10" size="1" readonly /><input type="button" onclick="incrementValue()" value="+" /></div> <br><div class="choose"><ul class="nav nav-pills nav-justified"><li><a href="{% url  prod.id %}" value=""><i class="fa fa-plus-square"></i>view product</a></li></ul></div></div></div></div></div>';
//             $("#cart_data").append(item_content);
//           }
//         }
//     //   } 
//     //   else {
//     //     $("#cart_data").empty();
//     //     {
//     //       let item_content =
//     //         '<div class="col-sm-4" ><div class="product-image-wrapper"> <div class="single-products"><div class="productinfo text-center"><img src="" alt="" /><p>`<b>Product Not Found</b>`</p></div></div></div></div></div>';
//     //       $("#cart_data").append(item_content);
//     //     }
//     //   }
//     },
//   });
// });




$(document).ready(function(){
	$("#loadMore").on('click',function(){
    debugger;
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#cart_data").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
    })
		});  
		// End
  })