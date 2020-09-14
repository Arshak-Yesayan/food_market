$(document).ready(function(){
    var form = $('#form_buying_product');
    form.on('submit', function(e){
        e.preventDefault();
        var nmb = $('#number').val();
        console.log(nmb);
        })
});

var add_cart = function(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            table = JSON.parse(this.response);
            console.log(table["result"]);
        }
    }
    xhttp.open("GET", `/products/add_cart?id=${id}&count=${document.getElementById(`number_${id}`).value}`, true);
    xhttp.send();
}