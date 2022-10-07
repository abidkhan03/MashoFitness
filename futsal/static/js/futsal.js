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
                url: "/api/deleteTeamRecord/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    console.log("success on delete" + data);
                    update_futsal_table(data)
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
        alert('Please select atleast one member to delete')
    }

}

function reloadPage() {
    window.location.reload();
    console.log("reload");
};





function SearchByFields() {
    let field = document.getElementById('search-by-field').value;
    let value = document.getElementById('search-by-value').value;
    if (field != '' && value != '') {
        $.ajax({
            method: "GET",
            url: "/api/SearchByFutsalField/",
            data: { "field": field, "value": value },
            success: function (data) {
                // console.log("success on search" + data);
                update_futsal_table(data)
            },
            error: function () {
                console.log('error');
            }

        })
    }
};

// function searchClick(){
//     let fromdate = document.getElementById('fromdate').value;
//     let todate = document.getElementById('todate').value;
//     console.log(fromdate);
//     console.log(todate);
//     if (fromdate != "" && todate != ""){
//         $.ajax({
//             method: "GET",
//             url: "/api/searchByExpenseDate/",
//             data: { "fromdate": fromdate, "todate": todate },
//             success: function (data) {
//                 console.log("success on search");
//                 console.log(data);
//                 update_table(data)

//             },
//             error: function () {
//                 console.log("error on get search by date");
//             }
//         });
//     }

// };

// function searchbymembername(){
//     let searchbyname = document.getElementById('searchbyname').value;
//     console.log(searchbyname);
//     $.ajax({
//         method: "GET",
//         url: "/api/searchByExpenseHeadOfAccount/",
//         data: { "searchbyname": searchbyname },
//         success: function (data) {
//             console.log("success on search");
//             console.log(data);
//             update_table(data)

//         },
//         error: function () {
//             console.log("error on get search by name");
//         }
//     });



// };




function update_futsal_table(data) {
    // console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        row ='<tr class="border-2 hover:bg-slate-300">'+
        '<td class="p-1">'+
            '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" >' +
        '</td>'+
        '<td class="p-1">'+elem['id']+'</td>'+
        '<td class="p-1">'+elem['member_created_at']+'</td>'+
        '<td class="p-1">'+elem['team_name']+'</td>'+
        '<td class="p-1">'+elem['captain_name']+'</td>'+
        '<td class="p-1">'+elem['contact_number']+'</td>'+
        '<td class="p-1">'+elem['team_attended_by']+'</td>'+

        '<td class="p-1">'+
        '<div class="flex flex-row gap-1">'+
            '<a href="/futsalMatch/?futsal-match='+elem['id']+'">'+
                '<button'+
                'class="bg-green-500 drop-shadow-md px-1 py-1 rounded-lg flex flex-row items-center rounded-br-none">'+
                '<span>Match</span>'+
                '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">'+
                '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />'+
                '</svg>'+
                '</button>'+
            '</a>'+
            '<a href="/teamDetails/?team-details='+ elem['id'] +'">'+
                '<button '+
                'class="bg-blue-600 drop-shadow-md px-1 py-1 rounded-lg inline-flex items-center rounded-br-none">'+
                '<span>Edit</span>'+
                '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 ml-2 w-4" fill="none"'+
                'viewBox="0 0 24 24" stroke="currentColor">'+
                '<path stroke-linecap="round" stroke-linejoin="round"'+
                'stroke-width="2"'+
                    ' d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                    '</svg>'+
                '</button>'+
            '</a>'+
            '</div>'+
        '</td>'+
    '</tr>' 
    all_rows += row;

    });

    $('#myTable tbody').html(all_rows);
}


function SearchByFutsalDate(date){
    $.ajax({
        method: "GET",
        url: "/api/SearchByFutsalDate/",
        data: { "date": document.getElementById('match-date').value },
        success: function (data) {
            console.log("success on search");
            var htmlcontainer = "";
            Object.keys(data).forEach(key => {
            elem = data[key];
            console.log(elem);
            if (elem['status']==false){
                console.log("false");
            htmlcontainer+=

            '<div class="flex flex-row gap-1 border border-teal-800">'+
            '<span>'+elem['time']+'&nbsp;'+elem['meridiem']+'</span>'+
            '</div>'

            
    }
        else{
            console.log("true");
            htmlcontainer+=
            '<div class="flex flex-row gap-1 border p-1 border-teal-900">'+
            '<span>'+elem['time']+ ' ' +elem['meridiem']+'</span>'+
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 text-green-700 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />'+
                '</svg>'+
            '</div>'


        
    }
        });
        var container = document.getElementById("booking-div-id");
        container.innerHTML = htmlcontainer;
        
        },
        error: function () {
            console.log("error on get search by date");
        }
    });
}


                                    