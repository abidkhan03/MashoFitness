member_id = null;
item_name = [];


function addToCart(id) {
    $.ajax({
        url: '/api/salesTerminal/addToCart',
        type: 'GET',
        data: {
            id: id
        },
        success: function (data) {
            CreateRows(data, id);
            updateCart();
        }
    });

}


function CreateRows(data, id) {
    try {
        if (item_name.includes(data['inventory_item_id']['item_name'])) {
            console.log(item_name)
            alert("Item already in cart");
        }
        else {
            item_name.push(data['inventory_item_id']['item_name']);
            // console.log(data['inventory_stock_available'])
            if (data['inventory_stock_available'] == 0) {
                alert("Item out of stock");
            }
            else {
                $('#myTable').find('tbody').append(
                    '<tr class="border-2 text-center">' +
                    '<td id="DeleteRow">' +
                    '<svg xmlns="http://www.w3.org/2000/svg"' +
                    'class="h-5 w-5 hover:border-blue-800 border-2 rounded-md text-red-900 cursor-pointer"' +
                    'fill="none" viewBox="0 0 24 24"' +
                    'stroke="currentColor">' +
                    '<path stroke-linecap="round" stroke-linejoin="round"' +
                    'stroke-width="2" d="M6 18L18 6M6 6l12 12" />' +
                    '</svg>' +
                    '</td>' +
                    '<td class="p-1">1</td>' +
                    '<td class="p-1">' + data['inventory_item_id']['item_code'] + '</td>' +
                    '<td class="p-1 product-name" name="helloworld">' + data['inventory_item_id']['item_name'] + '</td>' +
                    '<td class="p-1 productPrice">' + data['inventory_item_id']['item_selling_price'] + '</td>' +
                    '<td class="p-1 quantity">1</td>' +
                    '<td class="p-1 inline-flex items-center space-x-1">' +
                    '<svg xmlns="http://www.w3.org/2000/svg" class="sub-btn h-5 w-5 border border-blue-400 hover:border-2 rounded-md cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />' +
                    '</svg>' +

                    ' <svg xmlns="http://www.w3.org/2000/svg" class="add-btn h-5 w-5 border border-blue-400 hover:border-2 rounded-md cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />' +
                    '</svg>' +
                    '</td>' +
                    '<td class="totaldiscount p-1"><input placeholder="0" class="discount w-10"  /></td>' +
                    '<td class="price p-1 font-semibold">' + data['inventory_item_id']['item_selling_price'] + '</td>' +
                    // '<td class="p-1 font-semibold" hidden>' + data['inventory_stock_available']+ '</td>' +
                    '</tr>'
                );
                $('#' + data['inventory_item_id']['item_name']).text(parseInt($('#' + data['inventory_item_id']['item_name']).text()) - 1);

            }
        }
    }
    catch (err) {
        $.ajax({
            url: '/api/salesTerminal/addToCartNonStock',
            type: 'GET',
            data: {
                id: id
            },
            success: function (data) {
                CreateNonStockRows(data);
                updateCart();
            }
        });
    }
}

function CreateNonStockRows(data) {
    if (item_name.includes(data['nonStock_item_name'])) {

        alert("Item already in cart");
    }
    else {
        item_name.push(data['nonStock_item_name']);
        $('#myTable').find('tbody').append(
            '<tr class="border-2 text-center">' +
            '<td id="DeleteRow">' +
            '<svg xmlns="http://www.w3.org/2000/svg"' +
            'class="h-5 w-5 hover:border-blue-800 border-2 rounded-md text-red-900 cursor-pointer"' +
            'fill="none" viewBox="0 0 24 24"' +
            'stroke="currentColor">' +
            '<path stroke-linecap="round" stroke-linejoin="round"' +
            'stroke-width="2" d="M6 18L18 6M6 6l12 12" />' +
            '</svg>' +
            '</td>' +
            '<td class="p-1">1</td>' +
            '<td class="p-1">' + data['nonStock_item_code'] + '</td>' +
            '<td class="p-1 product-name">' + data['nonStock_item_name'] + '</td>' +
            '<td class="p-1 productPrice">' + data['nonStock_item_selling_price'] + '</td>' +
            '<td class="p-1 quantity">1</td>' +
            '<td class="p-1 inline-flex items-center space-x-1">' +
            '<svg xmlns="http://www.w3.org/2000/svg" class="sub-btn h-5 w-5 border border-blue-400 hover:border-2 rounded-md cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />' +
            '</svg>' +

            ' <svg xmlns="http://www.w3.org/2000/svg" class="add-btn h-5 w-5 border border-blue-400 hover:border-2 rounded-md cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />' +
            '</svg>' +
            '</td>' +
            '<td class="totaldiscount p-1"><input placeholder="0" class="discount w-10"  /></td>' +
            '<td class="price p-1 font-semibold">' + data['nonStock_item_selling_price'] + '</td>' +
            '</tr>'
        );
    }



}



$(document).ready(function () {
    // code to read selected table row cell data (values).
    $("#myTable").on('click', '.sub-btn', function () {
        // get the current row
        var currentRow = $(this).closest("tr");
        if (parseInt($('#' + currentRow.find("td:eq(3)").text()).text()) != 'inf') {
            if (parseInt(currentRow.find("td:eq(5)").text()) != 1) {
                var col4 = currentRow.find("td:eq(4)").text(); // get current row 4thTD
                var count = parseInt(currentRow.find("td:eq(5)").text()) - 1; // get current row 5thTD
                currentRow.find("td:eq(5)").text(count);
                currentRow.find("td:eq(8)").text(count * col4); // get current row 4thTD
                updateCart();
                // if (parseInt($('#'+currentRow.find("td:eq(3)").text()).text()) <= 0) {
                $('#' + currentRow.find("td:eq(3)").text()).text(parseInt($('#' + currentRow.find("td:eq(3)").text()).text()) + 1);
                // }
                // else {
                //     alert("Item out of stock");
                // }
            }
            else {
                alert("you must pick at least 1 item");
            }
        }
        else {
            var col4 = currentRow.find("td:eq(4)").text(); // get current row 4thTD
            var count = parseInt(currentRow.find("td:eq(5)").text()) - 1; // get current row 5thTD
            currentRow.find("td:eq(5)").text(count);
            currentRow.find("td:eq(8)").text(count * col4); // get current row 4thTD
            updateCart();
        }
        // $('#available-stock').text(parseInt($('#available-stock').text()) - 1);
        //  console.log(col4);
    });
    $("#myTable").on('click', '.add-btn', function () {
        // get the current row
        // co
        var currentRow = $(this).closest("tr");
        // console.log(document.getElementById(currentRow.find("td:eq(3)").text()).innerHTML);
        if (document.getElementById(currentRow.find("td:eq(3)").text()).innerHTML != 'inf') {
            if (parseInt($('#' + currentRow.find("td:eq(3)").text()).text()) > 0) {
                var col4 = currentRow.find("td:eq(4)").text(); // get current row 4thTD
                var count = parseInt(currentRow.find("td:eq(5)").text()) + 1; // get current row 5thTD
                currentRow.find("td:eq(5)").text(count);
                currentRow.find("td:eq(8)").text(count * col4); // get current row 4thTD
                updateCart();
                $('#' + currentRow.find("td:eq(3)").text()).text(parseInt($('#' + currentRow.find("td:eq(3)").text()).text()) - 1);
            }
            else {
                alert("Out of Stock");
            }
        }
        else {
            var col4 = currentRow.find("td:eq(4)").text(); // get current row 4thTD
            var count = parseInt(currentRow.find("td:eq(5)").text()) + 1; // get current row 5thTD
            currentRow.find("td:eq(5)").text(count);
            currentRow.find("td:eq(8)").text(count * col4); // get current row 4thTD
            updateCart();
        }

        // $('#'+currentRow.find("td:eq(3)").text()).text(parseInt($('#'+currentRow.find("td:eq(3)").text()).text()) - 1);
        // console.log($('#available-stock').text());
        // document.getElementById('available-stock').innerHTML = parseInt($('#available-stock').text()) + 1;
    });

});


(function () {
    "use strict";

    $("table").on("change", "input", function () {
        var row = $(this).closest("tr");
        var discount = parseFloat(row.find(".discount").val());
        var price = parseFloat(row.find(".price").text());
        var quantity = parseFloat(row.find(".quantity").text());
        var productprice = parseFloat(row.find(".productPrice").text());
        if (isNaN(discount)) {
            discount = 0;
            row.find(".price").text(productprice * quantity);
            updateCart();
        }
        else {
            var total = price - discount;
            row.find(".price").text(total);
            updateCart();
        }
    });
})();

$("#myTable").on("click", "#DeleteRow", function () {
    item_name.pop($(this).closest("tr").find(".product-name").text());
    if (document.getElementById($(this).closest("tr").find(".product-name").text()).innerHTML != 'inf') {
        // console.log($(this).closest("tr").find(".quantity").text());
        
        $('#' + $(this).closest("tr").find(".product-name").text()).
        text(parseInt($('#' + $(this).closest("tr").find(".product-name").text()).
        text()) + parseInt($(this).closest("tr").find(".quantity").text()));
    }
    $(this).closest("tr").remove();
    updateCart();

});

function updateCart() {
    const rows = document.querySelectorAll("#myTableBody > tr");
    var total = 0;
    var discount = 0;
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        if (row.querySelectorAll("td > input")[0].value != "") {
            discount += parseFloat(row.querySelectorAll("td > input")[0].value);
        }
        total += parseFloat(row.querySelector(".price").textContent);
    }
    document.getElementById("total-price").innerHTML = total; //total;
    document.getElementById("total-discount").innerHTML = discount; //total discount
    document.getElementById("subtotal").innerHTML = total + discount; //subtotal
    document.getElementById("amount-paid").innerHTML = total;
}


function searchItemInSalesTerminal(value) {
    $.ajax({
        url: '/api/searchItemInSalesTerminal/',
        method: 'GET',
        data: {
            'item_name': value
        },
        success: function (data) {
            console.log("stock")

            $('#item-main-div').empty();
            // if (data['Stock']) {
            //     Object.keys(data['Stock']).forEach(key => {
            //         var name = data['Stock'][key]['item_name']
            //         $('#item-main-div').append(
            //             '<div onclick="addToCart(\'' + name + '\')"' +
            //             'class="px-3 py-3 flex flex-col hover:border-2 border-blue-200 cursor-pointer bg-gray-200 rounded-md h-32 justify-between">' +
            //             '<div>' +
            //             '<div class="font-bold text-gray-800">' + data['Stock'][key]['item_name'] + '</div>' +
            //             '<span class="font-light text-sm text-gray-400">' + data['Stock'][key]['item_category'] + '</span>' +
            //             '</div>' +
            //             '<div class="flex flex-row justify-between items-center">' +
            //             '<span class="self-end font-bold text-lg text-yellow-500">' + data['Stock'][key]['item_selling_price'] + '</span>' +
            //             '<img src=' + data['Stock'][key]['item_image'] + ' class="h-14 object-cover rounded-md" alt="">' +
            //             '</div></div>');
            //     })

            // }
            // else if (data['NonStock']) {
            //     console.log("non stock");
            //     var name = data['NonStock']["nonStock_item_name"]
            //     Object.keys(data['NonStock']).forEach(key => {
            //         // console.log(key)÷
            //         $('#item-main-div').append(
            //             '<div onclick="addToCart(' + name + ')"' +
            //             'class="px-3 py-3 flex flex-col hover:border-2 border-blue-200 cursor-pointer bg-gray-200 rounded-md h-32 justify-between">' +
            //             '<div>' +
            //             '<div class="font-bold text-gray-800">' + data['NonStock'][key]['nonStock_item_name'] + '</div>' +
            //             '<span class="font-light text-sm text-gray-400">' + data['NonStock'][key]['nonStock_item_category'] + '</span>' +
            //             '</div>' +
            //             '<div class="flex flex-row justify-between items-center">' +
            //             '<span class="self-end font-bold text-lg text-yellow-500">' + data['NonStock'][key]['nonStock_item_selling_price'] + '</span>' +
            //             '<img src=' + data['NonStock']['nonStock_item_image'] + ' class="h-14 object-cover rounded-md" alt="">' +
            //             '</div></div>');
            //     })
            // }
            // else {
                console.log('else');
                Object.keys(data['Both']).forEach(key => {
                    var name = data['Both'][key]['item_name']
                    console.log(data['Both'][key]);
                    $('#item-main-div').append(
                        '<div onclick="addToCart(\'' + name + '\')"' +
                        'class="px-3 py-3 flex flex-col hover:border-2 border-blue-200 cursor-pointer bg-gray-200 rounded-md h-32 justify-between">' +
                        '<div>' +
                        '<div class="font-bold text-gray-800">' + data['Both'][key]['item_name'] + '</div>' +
                        '<span class="font-light text-sm text-gray-400">' + data['Both'][key]['item_category'] + '</span>' +
                        '<span class="text-sm" id="'+name+'">' + data['Both'][key]['item_stock'] + '</span>' +
                        // ' <span class="text-sm" id="coca cola">inf</span>'+
                        '</div>' +
                        '<div class="flex flex-row justify-between items-center">' +
                        '<span class="self-end font-bold text-lg text-yellow-500">' + data['Both'][key]['item_price'] + '</span>' +
                        '<img src=' + data['Both'][key]['item_image'] + ' class="h-14 object-cover rounded-md" alt="">' +
                        '</div></div>');
                });
            // }
        }
    });
}

function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
    member_id = checkbox.value
    console.log("member_id", member_id)
}

function memberSelection() {
    // console.log(member_id)
    const rows = document.querySelectorAll("#memberTableId > tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        id = row.querySelectorAll("td > input")[0].value
        // console.log(row.querySelector(".member-name-row").textContent)
        if (id == member_id) {
            // console.log(row.querySelector(".member-dues-row").textContent)
            document.getElementById("member-id").innerHTML = row.querySelector(".member-id-row").textContent;
            document.getElementById("Member-name").innerHTML = row.querySelector(".member-name-row").textContent;
            document.getElementById("Member-dues").innerHTML = row.querySelector(".member-dues-row").textContent;
        }
    }

}

function orderSelection() {
    // console.log(member_id)
    const rows = document.querySelectorAll("#orderTableId > tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        id = row.querySelectorAll("td > input")[0].value
        if (id == member_id) {
            orderDetailsModel(id)
        }
    }

}

function MemberSearchByName() {
    $.ajax({
        url: '/api/searchbynameCafeteriaCustomer/',
        method: 'GET',
        data: {
            'searchbyname': document.getElementById("search-memberName").value
        },
        success: function (data) {
            // console.log(data);
            let row;
            let all_rows = '';

            Object.keys(data).forEach(key => {
                elem = data[key];
                // console.log(elem);
                row =
                    '<tr>' +
                    '<td class="p-2">' +
                    '<input onclick="onlyOne(this)" value="' + elem['id'] + '" type="checkbox" name="check"' +
                    'class="cursor-pointer rounded-md ">' +
                    '</td>' +
                    '<td class="p-2">' + elem['customer_SerialNo'] + '</td>' +
                    '<td class="p-2 member-name-row">' + elem['customer_name'] + '</td>' +
                    '<td class="p-2">' + elem['customer_contact'] + '</td>' +
                    '</tr>'

                all_rows = all_rows + row;
            });

            $('#myTableCustomers tbody').html(all_rows);
        },
        error: function (data) {
            console.log('error in row add', data)
        }
    });
}

function OrderSearchByName() {
    $.ajax({
        url: '/api/searchbynameCafeteriaOrder/',
        method: 'GET',
        data: {
            'searchbyname': document.getElementById("search-memberNameForOrder").value
        },
        success: function (data) {
            // console.log(data);
            let row;
            let all_rows = '';

            Object.keys(data).forEach(key => {
                elem = data[key];
                // console.log(elem);
                row =
                    '<tr>' +
                    '<td class="p-2">' +
                    '<input onclick="onlyOne(this)" value="' + elem['id'] + '" type="checkbox" name="check"' +
                    'class="cursor-pointer rounded-md ">' +
                    '</td>' +
                    '<td class="p-1">' + elem['id'] + '</td>' +
                    '<td class="p-1">' + elem['order_date'] + '</td>' +
                    '<td class="p-1">' + elem['customer_id']['customer_name'] + '</td>' +
                    '<td class="p-1">' + elem['order_total_discount'] + '</td>' +
                    '<td class="p-1">' + elem['order_total_price'] + '</td>' +
                    '<td class="p-1 bg-green-200 m-3 drop-shadow-md rounded-xl rounded-br-none">' + elem['order_status'] + '</td>' +
                    '</tr>'

                all_rows = all_rows + row;
            });

            $('#myTableOrder tbody').html(all_rows);
        },
        error: function (data) {
            console.log('error in row add', data)
        }
    });
}

function submitForm() {
    console.log("success");
    var values = [];
    $('#myTableBody').find('tr').each(function () {
        console.log($(this).find('td')[2].innerHTML);
        values.push({
            itemName: $(this).find('td')[3].innerHTML,
            quantity: $(this).find('td')[5].innerHTML,
            discount: $(this).find('input')[0].value,
            totalPrice: $(this).find('td')[8].innerHTML
        });
    });
    var myJSON = JSON.stringify({ 'data': values });
    console.log(myJSON);
    // POST - send JSON data to Python/Django server
    $.ajax({
        url: "/api/CafeteriaOrderPlacement",
        type: "GET",
        datatype: 'json',
        data: JSON.stringify({
            "object": values,
            "member-id": document.getElementById("member-id").innerHTML,
            "total-price": document.getElementById("total-price").innerHTML,
            "total-discount": document.getElementById("total-discount").innerHTML,

        }),
        // async: false,
        success: function () {
            console.log('Your data is saved :)');
        },
        error: function () {
            console.log('Error occured :(');
        }
    });
}

function submitForm() {
    console.log("success");
    var values = [];
    $('#myTableBody').find('tr').each(function () {
        console.log($(this).find('td')[2].innerHTML);
        values.push({
            itemName: $(this).find('td')[3].innerHTML,
            quantity: $(this).find('td')[5].innerHTML,
            discount: $(this).find('input')[0].value,
            totalPrice: $(this).find('td')[8].innerHTML
        });
    });
    if (values.length == 0) {
        alert("Please select at least one item");
        return;
    }
    else {
        swal({
            title: "Are you sure. To Add Cashless Credit?",
            text: "Once you Ok, Then Payment added to Mashoo account!",
            icon: "warning",
            buttons: true,
            dangerMode: false,
        })
            .then((willDelete) => {
                // window.alpine_data.openViewCafeteriaBillModal();
                if (willDelete) {
                    swal("Order Completed  ", {
                        icon: "success",
                    });
                    // var myJSON = JSON.stringify({ 'data': values });
                    // POST - send JSON data to Python/Django server
                    $.ajax({
                        url: "/api/CafeteriaOrderPlacement",
                        type: "GET",
                        datatype: 'json',
                        data: JSON.stringify({
                            "object": values,
                            "member-id": document.getElementById("member-id").innerHTML,
                            "total-price": document.getElementById("total-price").innerHTML,
                            "total-discount": document.getElementById("total-discount").innerHTML,

                        }),
                        // async: false,
                        success: function () {
                            console.log('Your data is saved :)');

                            $("#myTableBody > tr").remove();
                            item_name = [];

                            // window.location.reload();
                        },
                        error: function () {
                            console.log('Error occured :(');
                        }
                    });

                } else {
                    swal("Order Cancelled!");
                }
            });
    }

}

function orderDetailsModel(id) {
    $.ajax({
        url: '/api/orderDetails/',
        method: 'GET',
        data: {
            'id': id
        },
        success: function (data) {
            orderDetailTable(data);
        },
        error: function (data) {
            console.log('error in row add', data)
        }
    });
}

function orderDetailTable(data) {
    // console.log(data);
    let row;
    let all_rows = '';
    var head =
        '<tr class="">' +
        '<th class="p-2">S No.</th>' +
        '<th class="p-2">Name</th>' +
        '<th class="p-2">Price</th>' +
        '<th class="p-2">Quantity</th>' +
        '<th class="p-2">Discount</th>' +
        '<th class="p-2">Total</th>' +
        '</tr>'

    Object.keys(data).forEach(key => {
        elem = data[key];
        // console.log(elem);
        row =
            '<tr>' +
            '<td class="p-1">' + elem['id'] + '</td>' +
            '<td class="p-1">' + elem['order_item_name'] + '</td>' +
            '<td class="p-1">' + elem['order_item_price'] + '</td>' +
            '<td class="p-1">' + elem['order_item_quantity'] + '</td>' +
            '<td class="p-1">' + elem['order_item_discount'] + '</td>' +
            '<td class="p-1">' + elem['order_item_total'] + '</td>' +
            '</tr>'

        all_rows = all_rows + row;
    });
    $('#myTableOrder thead').html(head);
    $('#myTableOrder tbody').html(all_rows);
}

function cashlessCredit() {
    console.log("success");
    var values = [];
    $('#myTableBody').find('tr').each(function () {
        console.log($(this).find('td')[2].innerHTML);
        values.push({
            itemName: $(this).find('td')[3].innerHTML,
            quantity: $(this).find('td')[5].innerHTML,
            discount: $(this).find('input')[0].value,
            totalPrice: $(this).find('td')[8].innerHTML
        });
    });
    if (values.length == 0) {
        alert("Please select at least one item");
        return;
    }
    else {
        swal({
            title: "Are you sure. To Add Cashless Credit?",
            text: "Once you Ok, Then Payment added to Mashoo account!",
            icon: "warning",
            buttons: true,
            dangerMode: false,
        })
            .then((willDelete) => {
                if (willDelete) {
                    swal("Order Completed  ", {
                        icon: "success",
                    });
                    $.ajax({
                        url: "/api/CafeteriaOrderPlacementAdmin",
                        type: "GET",
                        datatype: 'json',
                        data: JSON.stringify({
                            "object": values,
                            "total-price": document.getElementById("total-price").innerHTML,
                            "total-discount": document.getElementById("total-discount").innerHTML,
                        }),
                        success: function () {
                            console.log('Your data is saved :)');
                            $("#myTableBody > tr").remove();
                            item_name = [];
                        },
                        error: function () {
                            console.log('Error occured :(');
                        }
                    });
                } else {
                    swal("Order Cancelled!");
                }
            });
    }

}

function ZeroCheck(id) {
    if (id != 0) {
        return id;
    }
    else {
        return 0;
    }
}


function PrintTable() {
    console.log('print tabel')
    const rows = document.querySelectorAll("#myTableBody > tr");
    if (rows.length == 0) {
        window.alpine_data.closeCafeteriaBillModel();
    }
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        console.log(row);
        // $('#printTable').append(row);
        $('#printTable').append(


            '<tr>' +
            // '<td class="p-1">' + row.children[1].innerHTML + '</td>' +
            // '<td class="p-1">' + row.children[2].innerHTML + '</td>' +
            '<td class="p-1">' + row.children[3].innerHTML + '</td>' +
            '<td class="p-1">' + row.children[4].innerHTML + '</td>' +
            '<td class="p-1">' + row.children[5].innerHTML + '</td>' +
            // '<td class="p-1">' + row.children[6].innerHTML + '</td>' +
            // '<td class="p-1">' + row.children[7].innerHTML + '</td>' +
            '<td class="p-1">' + ZeroCheck(row.querySelectorAll("td > input")[0].value) + '</td>' +
            '<td class="p-1">' + row.children[8].innerHTML + '</td>' +
            '</tr>'
        );
    }

};
