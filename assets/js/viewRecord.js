
var today = new Date();

document.getElementById("today-date").innerHTML = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
function searchClick() {
    let fromdate = document.getElementById('fromdate').value;
    let todate = document.getElementById('todate').value;
    let user = document.getElementById("name").value;
    console.log(user)
    console.log(fromdate);
    console.log(todate);
    if (fromdate != "" && todate != "") {
        $.ajax({
            method: "GET",
            url: "/api/searchBillDate/",
            data: { "fromdate": fromdate, "todate": todate, "id": user },
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
function reloadPage() {
    window.location.reload();
    console.log("reload");
};

function ViewBillCall(id) {
    $.ajax({
        method: "GET",
        url: "/api/ViewBillCall/",
        data: { "id": id },
        success: function (data) {
            console.log("success on bill record");
            document.getElementById("b-inv").innerHTML = data['id'];
            document.getElementById("b-contact").innerHTML = data['fee_id']['member_id']['member_contact'];
            document.getElementById("b-category").innerHTML = data['subscription_id']['category_name'];
            document.getElementById("b-membership-type").innerHTML = data['subscription_id']['category_class'];
            document.getElementById("b-paid-date").innerHTML = data['start_date'];
            document.getElementById("b-total").innerHTML = data['payable'];
            document.getElementById("b-recieved").innerHTML = data['paid'];
            document.getElementById("b-remaining").innerHTML = data['remaining'];
        },
        error: function () {
            console.log("error on get bill record");
        }
    });


};


function update_table(data) {
    console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem['member_name']);
        row =
            '<tr class="text-left text-md border-2 hover:bg-slate-300">' +
            '<td class="p-2">' + elem['id'] + '</td>' +
            '<td class="p-2">' + elem['subscription_id']['category_months'] + '</td>' +
            '<td class="p-2">' + elem['start_date'] + '</td>' +
            '<td class="p-2">' + elem['end_date'] + '</td>' +
            '<td class="p-2">' + elem['amount'] + '</td>' +
            '<td class="p-2">' + elem['discount'] + '</td>' +
            '<td class="p-2">' + elem['payable'] + '</td>' +
            '<td class="p-2">' + elem['bill_created_at'] + '</td>' +
            '<td class="p-2">' + elem['paid'] + '</td>' +
            '<td class="p-2">' + elem['remaining'] + '</td>' +
            '<td class="p-1">' +
            '<div class="grid grid-rows-1 gap-1">' +
            '<div class="flex flex-row w-20">' +
            '<button x-on:click.prevent="openViewBillModal(elem["id"])"' +
            'class="bg-red-400 drop-shadow-md px-1 rounded-lg rounded-br-none">View Bill</button>' +
            '</div>' +
            '</div>' +
            '</td>' +
            '</tr>'
        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows);
};

const $printPaymentBill = document.querySelector("#printPaymentBill");
$printPaymentBill.addEventListener("click", () => {
    window.print();
});

function sendDeleteRequest(id) {
    // console.log(id);

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
            swalWithBootstrapButtons.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
            $.ajax({
                method: "GET",
                url: "/api/deleteBill/",
                data: { "id": id },
                success: function (data) {
                    console.log("success on delete");
                    update_table(data)
                    reloadPage();
                },
                error: function () {
                    console.log("error on delete");
                }
            });

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
};
