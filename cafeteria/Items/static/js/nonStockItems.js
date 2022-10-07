
function reloadPage() {
    window.location.reload();
    console.log("reload");
};

function SearchByStockField() {
    let field = document.getElementById('search-by-field').value;
    let value = document.getElementById('search-by-value').value;
    if (field != '' && value != '') {
        $.ajax({
            method: "GET",
            url: "/api/SearchByStockField/",
            data: { "field": field, "value": value },
            success: function (data) {
                // console.log("success on search" + data);
                update_table(data)
            },
            error: function () {
                console.log('error');
            }

        })
    }
};


function update_table(data){
    console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        row = '<tr class="text-left hover:bg-red-200">'+
        '<td class="p-2">'+
            '<div class="float-left hover:text-red-600">'+
                '<span @click="openUpdateModal">'+
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                    '</svg>'+
                '</span>'+
            '</div>'+
        '</td>'+
        '<td class="p-2">'+elem['nonStock_item_code']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_name']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_unit']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_purchase_price']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_selling_price']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_category']+'</td>'+
        '<td class="p-2">'+elem['nonStock_item_status']+'</td>'+

    '</tr>'
                                    
    all_rows = all_rows + row;
    });
    $('#myTable tbody').html(all_rows);
}

function onItemCode(data){
    var item_code = data.value;
    // console.log(item_code);
    // document.getElementById("item-barcode").innerHTML = item_code;
    JsBarcode("#barcode", item_code);
    // console.log(JsBarcode);
    $.ajax({
        method: "GET",
        url: "/api/NonStockItemCodeCheck/",
        data: { "item_code": item_code},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#item-code').removeClass('text-red-500');
            $('#item-code').addClass('text-green-500');
            $('#item-code').text('Available');
        }else{
            $('#item-code').removeClass('text-green-500');
            $('#item-code').addClass('text-red-500');
            $('#item-code').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

function ItemNameCheck(data){
    var item_name = data.value;
    $.ajax({
        method: "GET",
        url: "/api/NonStockItemNameCheck/",
        data: { "item_name": item_name},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#item-name').removeClass('text-red-500');
            $('#item-name').addClass('text-green-500');
            $('#item-name').text('Available');
        }else{
            $('#item-name').removeClass('text-green-500');
            $('#item-name').addClass('text-red-500');
            $('#item-name').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

function onItemCodeUpdate(data){
    var item_code = data.value;
    // console.log(item_code);
    // document.getElementById("item-barcode").innerHTML = item_code;
    JsBarcode("#barcode", item_code);
    // console.log(JsBarcode);
    $.ajax({
        method: "GET",
        url: "/api/NonStockItemCodeCheck/",
        data: { "item_code": item_code},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#update-item-code').removeClass('text-red-500');
            $('#update-item-code').addClass('text-green-500');
            $('#update-item-code').text('Available');
        }else{
            $('#update-item-code').removeClass('text-green-500');
            $('#update-item-code').addClass('text-red-500');
            $('#update-item-code').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

function ItemNameCheckUpdate(data){
    var item_name = data.value;
    $.ajax({
        method: "GET",
        url: "/api/NonStockItemNameCheck/",
        data: { "item_name": item_name},
        success: function (data) {
        // console.log(data);
        if(data['status']=='success'){
            $('#update-item-name').removeClass('text-red-500');
            $('#update-item-name').addClass('text-green-500');
            $('#update-item-name').text('Available');
        }else{
            $('#update-item-name').removeClass('text-green-500');
            $('#update-item-name').addClass('text-red-500');
            $('#update-item-name').text('Not Available');
        }
        },
        error: function () {
            console.log('error');
        }
    });
    
}

// function on NonStock Item Code Update
function update_query_call_nonstock(id){
    $.ajax({
        method: "GET",
        url: "/api/UpdateNonStockQueryCall/",
        data: { "nonStock-id": id},
        success: function (data) {
            Object.keys(data).forEach(key => {
            elem = data[key];
            console.log(elem['nonStock_item_image']);
            
            document.getElementById("update-id").value=elem['id'];

            document.getElementById("update-item-code").value=elem['nonStock_item_code'];
            document.getElementById("update-item-name").value=elem['nonStock_item_name'];
            document.getElementById("update-item-unit").value=elem['nonStock_item_unit'];
            document.getElementById("update-item-category").value=elem['nonStock_item_category'];
            document.getElementById("update-item-brand").value=elem['nonStock_item_brand'];
            document.getElementById("update-item-manufacturer").value=elem['nonStock_item_manufacturer'];
            document.getElementById("update-purchase-price").value=elem['nonStock_item_purchase_price'];
            document.getElementById("update-item-selling-price").value=elem['nonStock_item_selling_price'];
            document.getElementById("update-status").value=elem['nonStock_item_status'];
            document.getElementById("update-image").src=elem['nonStock_item_image'];
            document.getElementById("update-item-description").value=elem['nonStock_item_description'];
            // document.getElementById("item-barcode").value=elem['item_code'];

            });
            
        },
        error: function () {
            console.log('error');
        }

    })
}