var delete_array = [];

function requestDelete(e) {
    console.log(delete_array);
    if (e.checked) {
        delete_array.push(parseInt(e.dataset.id));
    } else {
        delete_array.splice(delete_array.indexOf(e.dataset.id), 1);
    }
    
}

// Delete a recrod function
function sendDeleteRequest() {
    if(delete_array.length > 0){

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
                url: "/api/deleteCustomer/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    console.log("success on delete"+data);
                    update_customer_table(data)
                    // reloadPage();
                },
                error: function() {
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
        alert('Please select atleast one member to delete')
    }
}

function reloadPage() {
    window.location.reload();
    console.log("reload");
};


function SearchByFields() {
    let field = document.getElementById('searchByType').value;
    let value = document.getElementById('searchByName').value;
    if (field != '' && value != '') {
        $.ajax({
            method: "GET",
            url: "/api/SearchByCustomerField/",
            data: { "field": field, "value": value },
            success: function (data) {
                // console.log("success on search" + data);
                update_customer_table(data)
            },
            error: function () {
                console.log('error');
            }

        })
    }
};

function update_customer_table(data) {
    // console.log(data);
    let row;
    let all_rows = '';
    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        row = '<tr class="border-2 hover:bg-slate-300">' +
            '<td class="p-2">' +
            '<input type="checkbox" class="cursor-pointer rounded-md"></td>' +
            '<td class="p-2">'+elem['id']+'</td>' +
            '<td class="p-2">'+elem['customer_account']+'</td>' +
            '<td class="p-2">'+elem['customer_name']+'</td>' +
            '<td class="p-2">'+elem['customer_contact']+'</td>' +
            '<td class="p-2">'+elem['customer_email']+'</td>' +
            '<td class="p-2">'+elem['customer_city']+'</td>' +
            '<td class="p-2">'+elem['customer_created_at']+'</td>' +
            '<td class="p-2">' +
            '<span class="px-2 py-1 font-semibold leading-tight text-orange-700 bg-orange-100 rounded-full dark:text-white dark:bg-orange-600"> '+elem['customer_status']+' </span>' +
            '</td>' +

            '<td class="p-2">' +
            '<div class="mr-5">' +
            '<a href="/updateCustomer/?customer='+elem['id']+'">' +
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">' +
           ' <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />' +
            '</svg>' +
                '</a >' +
            '</div >' +
        '</td >' +
    '</tr >'
            all_rows += row;
    });
    $('#myTable tbody').html(all_rows);
}


function getPaymentChange(){
        let dues = document.getElementById("dues").value;
        let paidamount = document.getElementById("payment").value;
        let remainingamount = dues - paidamount
        document.getElementById("remaining").value = remainingamount;
        
    };


