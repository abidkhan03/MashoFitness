function reload() {
    window.location.reload();
}


// function rowSelected(id) {
//     $.ajax({
//         url: '/api/cafeteria/salesReturn/get_sale/' + id,
//         type: 'GET',
//         // dataType: 'json',
//         success: function (data) {
//             console.log("data ", data)
//             // console.log(data[0]['customer_id'])
//             $('#salesSubtotal').val(data[0]['order_id']['order_total_price']);
//             $('#salesDiscount').val(data[0]['order_id']['order_total_discount']);
//             $('#salesTotal').val(data[0]['order_id']['order_total_price'] - data[0]['order_id']['order_total_discount']);
//             $('#salesDate').val(data[0]['salesReturn_date']);
//             if (data[0]['order_id']['customer_id'] != null) {
//                 $('#saleSCustomer').val(data[0]['order_id']['customer_id']['customer_name']);
//             }
//             else {
//                 $('#saleSCustomer').val("Walking Customer");
//             }
//             $('#salesStatus').val(data[0]['order_status']);
//             $('#sale-return-id').val(data[0]['order_id']['id']);
//             // $('#sale_items').empty();
//         },
//         error: function (data) {
//             alert('Error');
//         }

//     });
// }

function searchSales(value) {
    var type = $('#searchType').find(":selected").text();
    console.log(type);
    if (type == "Customer Name") {
        $.ajax({
            url: '/api/cafeteria/salesReturn/search_sales_customer/',
            type: 'GET',
            data: { 'customer_name': value.value },
            // dataType: 'json',
            success: function (data) {
                createTable(data);
            },
            error: function (data) {
                console.log("not found")
            },
        });
    }
    else if (type == "Invoice Number") {
        $.ajax({
            url: '/api/cafeteria/salesReturn/search_sales_invoiceID/' + value.value,
            type: 'GET',
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
    $('#salesTable tbody').empty();
    for (var i = 0; i < data.length; i++) {
        var row = "<tr class='text-left hover:bg-red-200'>";
        // row += '<td class="p-2">'+
        // '<span onclick="rowSelected(' + data[i]['order_id']['id'] + ')" @click="openViewCafeteriaSalesModal">' +
        //     '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"' +
        //     'fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
        //     '<path stroke-linecap="round" stroke-linejoin="round"' +
        //     'stroke-width="2"' +
        //     'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />' +
        //     '</svg>' +
        //     '</span>' +
        //     '</td>';


        row += "<td class='p-2'>" + data[i]['order_id']['id'] + "</td>";
        if (data[i]['order_id']['customer_id'] != null) {
            row += "<td class='p-2'>" + data[i]['order_id']['customer_id']['customer_name'] + "</td>";
        }
        else {
            row += "<td class='p-2'>Walking Customer</td>";
        }
        row += "<td class='p-2'>" + data[i]['salesReturn_date'] + "</td>";
        row += "<td class='p-2'>" + data[i]['order_id']['order_total_price'] + "</td>";
        // row += "<tdclass='p-2'>" + data[i]['order_total_price'] + "</td>";
        // console.log(data[i]['order_total_price'])
        row += "<td class='p-2'>" + data[i]['order_id']['order_total_discount'] + "</td>";
        let total=data[i]['order_id']['order_total_price']-data[i]['order_id']['order_total_discount'];
        row += "<td class='p-2'>" + total  + "</td>";
        // console.log(data[i]['order_total_price'] - data[i]['order_total_discount'] )
        // row += "<td class='p-2'>" + data[i]['order_total_price'] - data[i]['order_total_discount'] + "</td>";
        row += "<td class='p-2'>" + data[i]['order_id']['order_status'] + "</td>";



        // row += "<td class='p-2'><button class='btn btn÷÷-primary' onclick='rowSelected(" + data[i]['order_id'] + ")'>View</button></td>";
        row += "</tr>";
        $('#salesTable').append(row);
    }
}

// function createTable(data) {
//     $('#salesTable').empty();
//     for (var i = 0; i < data.length; i++) {
//         var row = "<tr class='text-left hover:bg-red-200'>";
//         row += '<td class="p-2">'
//         '<span onclick="rowSelected(' + data[i]['order_id'] + ')" @click="openViewCafeteriaSalesModal">' +
//             '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"' +
//             'fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
//             '<path stroke-linecap="round" stroke-linejoin="round"' +
//             'stroke-width="2"' +
//             'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />' +
//             '</svg>' +
//             '</span>' +
//             '</td>';


//         row += "<td class='p-2'>" + data[i]['order_id'] + "</td>";
//         if (data[i]['customer_id'] != null) {
//             row += "<td class='p-2'>" + data[i]['customer_id']['customer_name'] + "</td>";
//         }
//         else {
//             row += "<td class='p-2'>Walking Customer</td>";
//         }
//         row += "<td class='p-2'>" + data[i]['order_date'] + "</td>";
//         row += "<tdclass='p-2'>" + data[i]['order_total_price'] + "</td>";
//         row += "<td class='p-2'>" + data[i]['order_total_discount'] + "</td>";
//         row += "<td class='p-2'>" + data[i]['order_total_price'] - data[i]['order_total_discount'] + "</td>";
//         row += "<td class='p-2'>" + data[i]['order_status'] + "</td>";



//         // row += "<td class='p-2'><button class='btn btn÷÷-primary' onclick='rowSelected(" + data[i]['order_id'] + ")'>View</button></td>";
//         row += "</tr>";
//         $('#salesTable').append(row);
//     }
// }
