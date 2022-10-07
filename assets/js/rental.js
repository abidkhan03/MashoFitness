
function getEndDate(data) {
    var end_date = new Date(document.getElementById("rent-pay-date").value);
    console.log(end_date);
    var getmonth = data.value 
    
    getmonth = parseInt(getmonth.replace(/[^\d.]/g, ''));
    end_date.setMonth(end_date.getMonth() + getmonth);
    document.getElementById('end_date').value = end_date.toISOString().slice(0, 10);

    var rent = new Number(document.getElementById("rent-amount").value);
    console.log(rent);

    document.getElementById('total-rent').value = rent * getmonth;
}




function reloadPage() {
    window.location.reload();
    console.log("reload");
};

function SearchByFields() {
    let field = document.getElementById('search-by-field').value;
    let value = document.getElementById('search-by-value').value;
    console.log(field, value);
    if (field != '' && value != '') {
        $.ajax({
            method: "GET",
            url: "/api/SearchByRentalField/",
            data: { "field": field, "value": value },
            success: function (data) {
                // console.log("success on search" + data);
                update_rental_table(data)
            },
            error: function () {
                console.log('error');
            }

        })
    }
};

// search select from start to end date function 
function searchClick(){
    let fromdate = document.getElementById('fromdate').value;
    let todate = document.getElementById('todate').value;
    console.log(fromdate);
    console.log(todate);
    if (fromdate != "" && todate != ""){
        $.ajax({
            method: "GET",
            url: "/api/searchByRentalDate/",
            data: { "fromdate": fromdate, "todate": todate },
            success: function (data) {
                console.log("success on search");
                console.log(data);
                update_rental_table(data)
            
            },
            error: function () {
                console.log("error on get search by date");
            }
        });
    }

};


var delete_array = [];

function requestDelete(e) {
    
    if (e.checked) {
        delete_array.push(parseInt(e.dataset.id));
    } else {
        delete_array.splice(delete_array.indexOf(e.dataset.id), 1);
    }
    console.log(delete_array);

}

function sendDeleteRequest() {
    if (delete_array.length > 0) {
        
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {

            $.ajax({
                method: "GET",
                url: "/api/deleteRentalRecord/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    console.log("success on delete" + data);
                    update_rental_table(data)
                },
                error: function () {
                    console.log('error');
                }

            })
        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'Cancelled',
                'Your imaginary file is safe :)',
                'error'
            )
        }
    })
    }
    else{
        alert('Please select atleast one record to delete')
    }

}

function update_rental_table(data){
    let row;
    let all_rows;

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        if (elem['payment_status']=="Paid"){
        row = '<tr class="border-2 hover:bg-slate-300">'+
        '<td class="p-2">'+
        '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" >' +
        '</td>'+
        '<td class="p-1">'+elem['created_at']+'</td>'+
        '<td class="p-1">'+elem['Full_name']+'</td>'+
        '<td class="p-1">'+elem['contact_no']+'</td>'+
        '<td class="p-1">'+elem['shop_no']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_amount']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_pay_date']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_duration']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_end_date']+'</td>'+
        '<td class="p-1">'+elem['rent_pay_by']+'</td>'+
        '<td class="p-2 px-3 py-1 font-semibold leading-tight text-black bg-green-400 rounded-full">'+elem['payment_status']+'</td>'+
        '<td class="p-1">'+elem['rent_attended_by']['employee_username']+'</td>'+
        '<td class="p-1">'+
            '<a href="/updateRental/?rent='+elem['id']+'">'+
                '<button'+
                    'class="bg-blue-600 drop-shadow-md px-1 py-[.5] rounded-lg inline-flex items-center rounded-br-none" name="edit-expense" value="edit-expense">'+
                    '<span>Edit</span>'+
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 ml-2 w-5" fill="none"'+
                        'viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"'+
                            'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                    '</svg>'+
                '</button>'+
            '</a>'+
        '</td>'+
    '</tr>'
}
    else if(elem['payment_status']=='Unpaid'){
        row = '<tr class="border-2 hover:bg-slate-300">'+
        '<td class="p-2">'+
        '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" >' +
        '</td>'+
        '<td class="p-1">'+elem['created_at']+'</td>'+
        '<td class="p-1">'+elem['Full_name']+'</td>'+
        '<td class="p-1">'+elem['contact_no']+'</td>'+
        '<td class="p-1">'+elem['shop_no']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_amount']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_pay_date']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_duration']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_end_date']+'</td>'+
        '<td class="p-1">'+elem['rent_pay_by']+'</td>'+
        '<td class="p-2 px-3 py-1 font-semibold leading-tight text-black bg-yellow-400 rounded-full">'+elem['payment_status']+'</td>'+
        '<td class="p-1">'+elem['rent_attended_by']['employee_username']+'</td>'+
        '<td class="p-1">'+
            '<a href="/updateRental/?rent='+elem['id']+'">'+
                '<button'+
                    'class="bg-blue-600 drop-shadow-md px-1 py-[.5] rounded-lg inline-flex items-center rounded-br-none" name="edit-expense" value="edit-expense">'+
                    '<span>Edit</span>'+
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 ml-2 w-5" fill="none"'+
                        'viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"'+
                            'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                    '</svg>'+
                '</button>'+
            '</a>'+
        '</td>'+
    '</tr>'
    }
    else{
        row = '<tr class="border-2 hover:bg-slate-300">'+
        '<td class="p-2">'+
        '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" >' +
        '</td>'+
        '<td class="p-1">'+elem['created_at']+'</td>'+
        '<td class="p-1">'+elem['Full_name']+'</td>'+
        '<td class="p-1">'+elem['contact_no']+'</td>'+
        '<td class="p-1">'+elem['shop_no']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_amount']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_pay_date']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_duration']+'</td>'+
        '<td class="p-1">'+elem['active_rent_id']['rent_end_date']+'</td>'+
        '<td class="p-1">'+elem['rent_pay_by']+'</td>'+
        '<td class="p-2 px-3 py-1 font-semibold leading-tight text-black bg-red-400 rounded-full">'+elem['payment_status']+'</td>'+
        '<td class="p-1">'+elem['rent_attended_by']['employee_username']+'</td>'+
        '<td class="p-1">'+
            '<a href="/updateRental/?rent='+elem['id']+'">'+
                '<button'+
                    'class="bg-blue-600 drop-shadow-md px-1 py-[.5] rounded-lg inline-flex items-center rounded-br-none" name="edit-expense" value="edit-expense">'+
                    '<span>Edit</span>'+
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 ml-2 w-5" fill="none"'+
                        'viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"'+
                            'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                    '</svg>'+
                '</button>'+
            '</a>'+
        '</td>'+
    '</tr>'
    }
    all_rows += row;
    });
    $('#myTable tbody').html(all_rows);
}

