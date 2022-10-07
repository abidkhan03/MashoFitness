add_array = null;
// function requestAdd(e) {
//     if (e.checked) {
//         add_array.push(parseInt(e.dataset.id));
//     } else {
//         add_array.splice(add_array.indexOf(e.dataset.id), 1);
//     }

// }

function update_query_call_inventory(id) {
    $.ajax({
        method: "GET",
        url: "/api/updateInventoryQueryCall/",
        data: { "inventory-id": id },
        success: function (data) {
            Object.keys(data).forEach(key => {
                elem = data[key];
                console.log(elem)

                document.getElementById("update-id").value = elem['id'];
                document.getElementById("item-code").value = elem['inventory_item_id']['item_code'];
                document.getElementById("item-name").value = elem['inventory_item_id.item_name'];
                document.getElementById("item-unit").value = elem['inventory_item_id.item_unit'];
                document.getElementById("unit-price").value = elem['inventory_unit_price'];
                document.getElementById("image").src = elem['inventory_unit_price']['item_image'];
                document.getElementById("net-price").value = elem['inventory_net_price'];
                document.getElementById("purchased-qty").value = elem['inventory_purchased_quantity'];
                document.getElementById("sub-total").value = elem['inventory_stock_available'];
                document.getElementById("item-total").value = elem['inventory_item_total'];
                document.getElementById("order-number").value = elem['inventory_order_number'];
                document.getElementById("reference-number").value = elem['inventory_reference_number'];
                document.getElementById("supplier").value = elem['supplier_id']['supplier_name'];
                // document.getElementById("available-stock").value = elem['inventory_stock_in_shop'];
            });

        },
        error: function () {
            console.log('error');
        }

    })
}
function addInventoryItem() {
    // console.log(add_array)
    if (add_array == null) {
        alert("Please select an item to add");
        window.alpine_data.closeModal();
    }
    else{
    $.ajax({
        method: "GET",
        url: "/api/updateInventoryQueryCall/",
        data: { "inventory-id": add_array },
        success: function (data) {
            // console.log(data)
            Object.keys(data).forEach(key => {
                elem = data[key];
                console.log(elem['supplier_id'])

                document.getElementById("update-id").value = elem['id'];
                document.getElementById("item-code").value = elem['inventory_item_id']['item_code'];
                document.getElementById("item-name").value = elem['inventory_item_id']['item_name'];
                document.getElementById("item-unit").value = elem['inventory_item_id']['item_unit'];
                // document.getElementById("unit-price").value = elem['inventory_unit_price'];
                document.getElementById("image").src = elem['inventory_item_id']['item_image'];
                // document.getElementById("net-price").value = elem['inventory_net_price'];
                // document.getElementById("purchased-qty").value = elem['inventory_purchased_quantity'];
                document.getElementById("sub-total").value = elem['inventory_stock_available'];
                // document.getElementById("item-total").value = elem['inventory_item_total'];
                // document.getElementById("order-number").value = elem['id'];
                // document.getElementById("reference-number").value = elem['id'];
                // document.getElementById("supplier").value = elem['supplier_id']['supplier_name'];
                // document.getElementById("available-stock").value = elem['inventory_stock_in_shop'];
            });

        },
        error: function () {
            console.log('error');
        }

    })
}
}

function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
    add_array = parseInt(checkbox.dataset.id);
}

function ImageLoder(data) {
    let file = data.files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
        console.log("update call ", e.target.result);
        document.getElementById('image').src = e.target.result;
        document.getElementById('update-image').src = e.target.result;
    }
    reader.readAsDataURL(file);

}
//  calculating the total price values 
document.getElementById("purchased-qty").onkeyup = function () {
    var unit_price = document.getElementById('unit-price').value;
    var purchased = document.getElementById('purchased-qty').value;
    var total = unit_price * purchased;
    document.getElementById('item-total').value = total;
};


function reload() {
    window.location.reload();
}

function searchInventory(value) {
    var type = $('#searchType').find(":selected").text();
    console.log(type);
    if (type == "Item Name") {
        $.ajax({
            url: '/api/cafeteria/inventory/search_inventory_ItemName/',
            type: 'GET',
            data: { 'item_name': value.value },
            // dataType: 'json',
            success: function (data) {
                createTable(data);
            },
            error: function (data) {
                console.log("not found")
            },
        });
    }
    else if (type == "Item Code") {
        $.ajax({
            url: '/api/cafeteria/inventory/search_inventory_ItemCode/',
            type: 'GET',
            data: { 'item_code': value.value },
            // dataType: 'json',
            success: function (data) {
                createTable(data);
            },
            error: function (data) {
                console.log("not found")
            },
        });
    }
    else {
        alert("Please select a search type");
    }

}

function createTable(data) {
    $('#InventoryTable tbody').empty();
    for (var i = 0; i < data.length; i++) {
        var row = "<tr class='text-left hover:bg-red-200'>";
        row += '<td class="p-2">' +
            '<input onclick="onlyOne(this)" data-id="'+ data[i]['id']+'" type="checkbox"' +
            'class="cursor-pointer rounded-md" name="check">' +
            '</td>';
        // row += '<td class="p-2">' +
        //     '<div class="float-left hover:text-red-600">' +
        //     '<span @click="openUpdateModal('+ data[i]['id']+', \'inventory\')">' +
        //     '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"' +
        //     'fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
        //     '<path stroke-linecap="round" stroke-linejoin="round"' +
        //     'stroke-width="2"' +
        //     'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />' +
        //     '</svg>' +
        //     '</span>' +
        //     '</div>' +
        //     '</td>';


        row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_code'] +'</td>';
        row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_name'] +'</td>';
        row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_unit'] +'</td>';
        row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_selling_price'] +'</td>';
        row += '<td class="p-2">'+ data[i]['inventory_stock_available'] +'</td>';
        // row += '<td class="p-2">'+ data[i]['inventory_stock_in_shop'] +'</td>';
        // row += '<td class="p-2">{{product.inventory_stock_in_shop}}</td>';


        // row += "<td class='p-2'>" + data[i]['id'] + "</td>";
        // if (data[i]['customer_id'] != null) {
        //     row += "<td class='p-2'>" + data[i]['customer_id']['customer_name'] + "</td>";
        // }
        // else {
        //     row += "<td class='p-2'>Walking Customer</td>";
        // }
        // row += "<td class='p-2'>" + data[i]['order_date'] + "</td>";
        // row += "<td class='p-2'>" + data[i]['order_total_price'] + "</td>";
        // // row += "<tdclass='p-2'>" + data[i]['order_total_price'] + "</td>";
        // // console.log(data[i]['order_total_price'])
        // row += "<td class='p-2'>" + data[i]['order_total_discount'] + "</td>";
        // let total = data[i]['order_total_price'] - data[i]['order_total_discount'];
        // row += "<td class='p-2'>" + total + "</td>";
        // // console.log(data[i]['order_total_price'] - data[i]['order_total_discount'] )
        // // row += "<td class='p-2'>" + data[i]['order_total_price'] - data[i]['order_total_discount'] + "</td>";
        // row += "<td class='p-2'>" + data[i]['order_status'] + "</td>";



        // row += "<td class='p-2'><button class='btn btn÷÷-primary' onclick='rowSelected(" + data[i]['order_id'] + ")'>View</button></td>";
        row += "</tr>";
        $('#InventoryTable').append(row);
    }
}

function checkOrderNumber(data){
    var item_name = data.value;
    $.ajax({
        method: "GET",
        url: "/api/checkOrderNumber/",
        data: { "item_name": item_name},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#order-number').removeClass('text-red-500');
            $('#order-number').addClass('text-green-500');
            $('#order-number').text('Available');
        }else{
            $('#order-number').removeClass('text-green-500');
            $('#order-number').addClass('text-red-500');
            $('#order-number').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

function checkOrderNumber(data){
    var code = data.value;
    $.ajax({
        method: "GET",
        url: "/api/checkOrderNumber/",
        data: { "code": code},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#order-number').removeClass('text-red-500');
            $('#order-number').addClass('text-green-500');
            $('#order-number').text('Available');
        }else{
            $('#order-number').removeClass('text-green-500');
            $('#order-number').addClass('text-red-500');
            $('#order-number').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

function checkRefferenceNumber(data){
    var code = data.value;
    $.ajax({
        method: "GET",
        url: "/api/checkRefferenceNumber/",
        data: { "code": code},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#reference-number').removeClass('text-red-500');
            $('#reference-number').addClass('text-green-500');
            $('#reference-number').text('Available');
        }else{
            $('#reference-number').removeClass('text-green-500');
            $('#reference-number').addClass('text-red-500');
            $('#reference-number').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}


function calculateTotal(data){
    var total=$('#item-total').val();
    // console.log(total-data.value);
    document.getElementById('remaining').value = total-data.value;
}

// function getSupplierDetails(data){
//     var supplierName= data.value;
//     $.ajax({
//         method: "GET",
//         url: "/api/getSupplierDetails/",
//         data: { "supplierName": supplierName},
//         success: function (data) {
//         console.log(data);

        
//         },
//         error: function () {
//             console.log('error');
//         }
//     });
    
// }