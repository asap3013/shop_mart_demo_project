$(document).ready(function(){
    $('.submitWidget').css("display", "none");
    $('.remove').css("display","none")
});


window.addEventListener('load', () => {
    const ship_amount = sessionStorage.getItem("ship_amt");
    document.getElementsByClassName('shipamt').innerHTML = ship_amount;
    const ftotal = sessionStorage.getItem("TOTAL");
    document.getElementById('ftotal').innerHTML = ftotal;
    

})

$(document).on('click', ".order", function () {
    var address = document.getElementById('hiddenaddress').value;
    let final_total =sessionStorage.getItem('TOTAL');
    let ship_amt = document.getElementsByClassName('shipamt')[0].innerHTML;
    let cod = document.getElementsByClassName('payload').innerHTML;
    let stripe = document.getElementsByClassName('payload').innerHTML;
    $.ajax({
        url: '/placeorder',
        data: {
            'address_id':address,
            'TOTAL': final_total,
            'ship_amt':ship_amt,
            'cod':cod,
            'stripe':stripe
        },
        dataType: 'json',
        success: function (res) {
            
        }
    });
});  


$(document).on('click', ".stripebutton", function () {
    var address = document.getElementById('hiddenaddress').value;
    let final_total =sessionStorage.getItem('TOTAL');
    let ship_amt = document.getElementsByClassName('shipamt')[0].innerHTML;
    let cod = document.getElementsByClassName('payload').innerHTML;
    let stripe = document.getElementsByClassName('payload').innerHTML;
    $.ajax({
        url: '/stripe',
        data: {
            'address_id':address,
            'TOTAL': final_total,
            'ship_amt':ship_amt,
            'cod':cod,
            'stripe':stripe
        },
        dataType: 'json',
        success: function (res) {
            
        }
    });
});  

