var delete_array = [];

function requestDelete(e) {
    console.log(delete_array);
    if (e.checked) {
        delete_array.push(parseInt(e.dataset.id));
    } else {
        delete_array.splice(delete_array.indexOf(e.dataset.id), 1);
    }
    
}


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
                url: "/api/deleteCafeteriaExpense/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    console.log("success on delete"+data);
                    update_table(data)
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





// function resultperpageValueChanged(){
//     let resultperpage = document.getElementById('resultperpage').value;
//     let searchbytype=document.getElementById('searchbytype').value;
   
//         $.ajax({
//             method: "GET",
//             url: "/api/searchByExpenseData/",
//             data: { "resultperpage": resultperpage, "searchbytype": searchbytype  },
//             success: function (data) {
//                 console.log("success on search");
//                 console.log(data);
//                 update_table(data)
            
//             },
//             error: function () {
//                 console.log("error on get search by data");
//             }
//         });
    
    
// };

function searchClick(){
    let fromdate = document.getElementById('fromdate').value;
    let todate = document.getElementById('todate').value;
    console.log(fromdate);
    console.log(todate);
    if (fromdate != "" && todate != ""){
        $.ajax({
            method: "GET",
            url: "/api/searchByCafeteriaExpenseDate/",
            data: { "fromdate": fromdate, "todate": todate },
            success: function (data) {
                console.log("success on search");
                console.log(data);
                update_table(data)
            
            },
            error: function () {
                console.log("error on get search by date");
            }
        });
    }

};

function searchbymembername(){
    let searchbyname = document.getElementById('searchbyname').value;
    console.log(searchbyname);
    $.ajax({
        method: "GET",
        url: "/api/searchByCafeteriaExpenseHeadOfAccount/",
        data: { "searchbyname": searchbyname },
        success: function (data) {
            console.log("success on search");
            console.log(data);
            update_table(data)
        
        },
        error: function () {
            console.log("error on get search by name");
        }
    });
};




function update_table(data) {
    console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem)
        row =

            '<tr class="border-2 hover:bg-slate-300">' +
                '<td class="p-2">' +
                    '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" onc>' +
                '</td>' +
                '<td class="p-2">'+ elem['date'] +'</td>'+
                '<td class="p-2">'+elem['account_head']+'</td>'+
                '<td class="p-2">'+elem['paid_amount']+'</td>'+
                '<td class="p-2">'+elem['payment_mode']+'</td>'+
                '<td class="p-2">'+elem['expenses_for']+'</td>'+
                '<td class="p-2">'+elem['description']+'</td>'+
                '<td class="p-2">'+elem['receipent_name']+'</td>'+
                '<td class="p-2" >'+
                        '<a href="/updateExpense/?data='+elem['id']+'">'+
                        '<button class="bg-blue-600 drop-shadow-md px-1 py-[.5] rounded-lg inline-flex items-center rounded-br-none" name="edit-expense" value="edit-expense">'+
                        '<span>Edit</span>'+
                        '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 ml-2 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">'+
                            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                        '</svg>'+
                    '</button>'+
                        '</a>'+
                '</td>'+
            '</tr>';

        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows);
}
