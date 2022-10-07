function inventory_query_call(id){
    $.ajax({
        method: "GET",
        url: "/api/InventoryQueryCall/",
        data: { "id": id},
        success: function (data) {
            Object.keys(data).forEach(key => {
            elem = data[key];
            console.log(elem)
            
            document.getElementById("update-id").value=elem['id'];
            document.getElementById("item-code").value=elem['item_code'];
            document.getElementById("item-name").value=elem['item_name'];
            document.getElementById("item-unit").value=elem['item_unit'];
            document.getElementById("item-selling-price").value=elem['item_selling_price'];
            document.getElementById("image").src=elem['item_image'];
            document.getElementById("update-remaining-days").value=elem['item_expiry_day'];
            });
            
        },
        error: function () {
            console.log('error');
        }

    })
}