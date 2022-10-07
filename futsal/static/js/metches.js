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
                url: "/api/deleteTeamMatch/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    update_match_table(data)
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

function SearchByStatus(e) {
    console.log(e.value);
    $.ajax({
        method: "GET",
        url: "/api/SearchByTeamMatchStatus/",
        data: { "status": e.value },
        success: function (data) {
            update_match_table(data)
        },
        error: function () {
            console.log('error');
        }

    })
}

function SearchByFields() {
    let field = document.getElementById('search-by-field').value;
    let value = document.getElementById('search-by-value').value;
    if (field != '' && value != '') {
        $.ajax({
            method: "GET",
            url: "/api/SearchByTeamMatchField/",
            data: { "field": field, "value": value },
            success: function (data) {
                // console.log("success on search" + data);
                update_match_table(data)
            },
            error: function () {
                console.log('error');
            }

        })
    }
};


function update_match_table(data){
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        row =
        '<tr class="border-2 hover:bg-slate-300">' +
        '<td class="p-1">' + 
            '<input  onclick="requestDelete(this)" data-id="'+elem['id']+'" type="checkbox" class="cursor-pointer rounded-md">' +
        '</td>' +
        '<td class="p-1">'+elem['id']+'</td>' +
        '<td class="p-1">'+elem['date']+'</td>' +
        '<td class="p-1">'+elem['team1']['team_name']+'</td>' +
        '<td class="p-1">'+elem['team2']['team_name']+'</td>' +
        '<td class="p-1">'+elem['booking_time']['time']+'</td>' +
        '<td class="p-1">'+elem['team1']['contact_number']+'</td>' +
        '<td class="p-1">'+elem['paid']+'</td>' +
        '<td class="p-1">admin</td>' +
        '<td class="p-1">'+
            '<a href="/matches/?match_done_row_id='+elem['id']+'">' +
                '<button class="bg-green-400 drop-shadow-md rounded-lg inline-flex items-center py-1 px-1 rounded-br-none">' +
                    '<span>Done</span>' +
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">' +
                        '<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />'+
                        '</svg>'+
                '</button>' +
            '</a>' +
            '<a href="/updateFutsalMatch/?match_edit_row_id='+elem['id']+'">' +
                '<button class="bg-blue-600 drop-shadow-md px-1 py-1 rounded-lg inline-flex items-center rounded-br-none">'+
                    '<span>Edit</span>' +
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 ml-2 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">'+
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                        '</svg>'+
                '</button>' +
            '</a>' +
        '</td>' +
        '</tr>'

    

        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows);






}

function searchByFutsalDate(date){
    $.ajax({
        method: "GET",
        url: "/api/searchByFutsalDate/",
        data: { "date": date.value },
        success: function (data) {
            update_match_table(data)
        },
        error: function () {
            console.log('error');
        }

    })
}