function reload() {
    window.location.reload();
}

function searchPurchases(value) {
    var type = $('#searchType').find(":selected").text();
    console.log(type);
    if (type == "Supllier Name") {
        $.ajax({
            url: '/api/cafeteria/purchases/search_purchasesReturn_supplierName/',
            type: 'GET',
            data: { 'supplier_name': value.value },
            // dataType: 'json',
            success: function (data) {
                createTable(data);
            },
            error: function (data) {
                console.log("not found")
            },
        });
    }
    else if (type == "Order Number") {
        $.ajax({
            url: '/api/cafeteria/purchases/search_purchasesReturn_orderNumber/',
            type: 'GET',
            data: { 'order_name': value.value },
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
    $('#ReturnTable tbody').empty();
    for (var i = 0; i < data.length; i++) {
        var row = '<tr class="text-left hover:bg-red-200">';
        row +='<td class="p-2">'+data[i]['purchases_id']['purchases_order_number']+'</td>';
        row +='<td class="p-2">'+data[i]['purchases_id']['purchases_reference_number']+'</td>';
        row +='<td class="p-2">'+data[i]['purchases_id']['purchases_supplier_id']['supplier_name']+'</td>';
        row +='<td class="p-2">'+data[i]['return_date']+'</td>';
        row +='<td class="p-2">'+data[i]['return_stock']+'</td>';
        row +='<td class="p-2">'+data[i]['tatal_price']+'</td>';
        row +='<td class="p-2">Returned</td>';
        row +='</tr >';


            // row += '<td class="p-2">' +
            //     '<input onclick="onlyOne(this)" data-id="'+ data[i]['id']+'" type="checkbox"' +
            //     'class="cursor-pointer rounded-md" name="check">' +
            //     '</td>';
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


            // row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_code'] +'</td>';
            // row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_name'] +'</td>';
            // row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_unit'] +'</td>';
            // row += '<td class="p-2">'+ data[i]['inventory_item_id']['item_selling_price'] +'</td>';
            // row += '<td class="p-2">'+ data[i]['inventory_stock_available'] +'</td>';
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
        $('#ReturnTable').append(row);
    }
}
