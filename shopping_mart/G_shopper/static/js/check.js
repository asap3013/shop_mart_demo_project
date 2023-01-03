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


$(document).on('click','.order',function () {
    var rates = document.getElementsByClassName('payload');
    var order_value;
    let ch = document.getElementById('checkouts')
    for(var i = 0; i < rates.length; i++){
        if(rates[i].checked){
            order_value = rates[i].value;
        }
    }

    if(order_value == "stripe"){
        var rates = document.getElementsByClassName('hiddenaddress');
        var rate_value;
        for(var i = 0; i < rates.length; i++){
        if(rates[i].checked){
            rate_value = rates[i].value;
            }
        }
        let final_total =sessionStorage.getItem('TOTAL');
        let ship_amt = document.getElementsByClassName('shipamt')[0].innerHTML;
        let cod = document.getElementsByClassName('payload').innerHTML;
        let stripe = document.getElementsByClassName('payload').innerHTML;
        
        $.ajax({
            type: "POST",
            url: '/stripe/',
            data: JSON.stringify({
                "address_id":rate_value,
                "total": final_total,
                "ship_amount":ship_amt,
                "cod":cod,
                "stripe":stripe,
            }),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                window.location.href = ''+response;
                 }
        });
    }

    else{
        debugger;
        var rates = document.getElementsByClassName('hiddenaddress');
        var rate_value;
        for(var i = 0; i < rates.length; i++){
        if(rates[i].checked){
            rate_value = rates[i].value;
        }}
        let final_total =sessionStorage.getItem('TOTAL');
        let ship_amt = document.getElementsByClassName('shipamt')[0].innerHTML;
        let csrftoken = '{{ csrf_token }}';

        $.ajax({
            type: "POST",
            headers:{'X-CSRFToken':csrftoken},
            url: '/cod/',
            data: {
                'address_id':rate_value,
                'TOTAL': final_total,
                'ship_amt':ship_amt,
            },
            dataType: 'json',
            success: function (data) {
                // window.location.href = 'http://127.0.0.1:8000/home'
            }
        });
    }
});
