var delete_array = [];

function instalmentValueChanged(instalment) {
    var paidamount = document.getElementById("paidamount");
    // var remainingamount = document.getElementById("remainingamount");
    if (instalment.checked){
    paidamount.style.display = "block";
    // remainingamount.style.display = instalment.checked ? "block" : "none";
    let paidamounts=document.getElementById("paidamounts");
    paidamounts.setAttribute("required", "true");
    let remainingamount=document.getElementById("remaining-amount");
    remainingamount.setAttribute("required", "true");
    }
    else{
        paidamount.style.display = "none";
        let paidamounts=document.getElementById("paidamounts");
        paidamounts.removeAttribute("required")
        let remainingamount=document.getElementById("remaining-amount");
        remainingamount.removeAttribute("required")
    }

};

function categoryClassChange(){
    let category_name=document.getElementById("membershipcategory").value
    let category_class=document.getElementById("membership-class").value
    let category_gender=document.getElementById("gender").value


    $.ajax({
        method: "GET",
        url: "/api/get_membershipCategory/",
        data:{
            "category_name":category_name,
            "category_class":category_class,
            "category_gender":category_gender
        },
        success: function (data) {
            Object.keys(data).forEach(key => {
                var value = data[key];
                document.getElementById("category-months").value=value['category_months'];
                document.getElementById("amount").value=value["category_fee"];
                document.getElementById("payableamount").value=value["category_fee"];
                getExpiry(value['category_months']);

            });
        },
        error: function () {
            console.log("error on get Membership Category months");
        }
    });



}



document.getElementById("discount").onchange = function () {
    var amount = document.getElementById('amount').value;
    var discount = document.getElementById('discount').value;
    var total = amount - discount;
    document.getElementById('payableamount').value = total;
};

document.getElementById("dateofbirth").onchange = function () {
    var Bdate = this.value;
    var Bday = +new Date(Bdate);
    document.getElementById('age').value = ~~((Date.now() - Bday) / (31557600000));
}

function getExpiry(data) {
    var expiry = new Date(document.getElementById("membership-start-date").value);
    console.log(expiry);
    var getmonth = data 
    
    getmonth = parseInt(getmonth.replace(/[^\d.]/g, ''));
    expiry.setMonth(expiry.getMonth() + getmonth);
    document.getElementById('expiry').value = expiry.toISOString().slice(0, 10);
}

document.getElementById("paidamounts").onchange = function(){
    let payableamount = document.getElementById("payableamount").value;
    let paidamount = document.getElementById("paidamounts").value;
    let remainingamount = payableamount - paidamount
    document.getElementById("remaining-amount").value = remainingamount;
    
};

// function payableOnChange(this){
//     let paidamount = document.getElementById("paid-amount").value;
//     alert(this.value)
//     alert(paidamount)
//     document.getElementById("remaining-amount").value=this.value - paidamount;
// }



function requestDelete(e) {
    if (e.checked) {
        delete_array.push(parseInt(e.dataset.id));
    } else {
        delete_array.splice(delete_array.indexOf(e.dataset.id), 1);
    }
    
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
            swalWithBootstrapButtons.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
              )
            $.ajax({
                method: "GET",
                url: "/api/deleteMember/",
                data: { "arr[]": delete_array },
                success: function (data) {
                    console.log("success on delete"+data);
                    update_table(data)
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
};





function resultperpageValueChanged(){
    let resultperpage = document.getElementById('resultperpage').value;
    let searchbytype=document.getElementById('searchbytype').value;
   
        $.ajax({
            method: "GET",
            url: "/api/searchbydata/",
            data: { "resultperpage": resultperpage, "searchbytype": searchbytype  },
            success: function (data) {
                console.log("success on search");
                console.log(data);
                update_table(data)
            
            },
            error: function () {
                console.log("error on get search by data");
            }
        });
    
    
};

function searchClick(){
    let fromdate = document.getElementById('fromdate').value;
    let todate = document.getElementById('todate').value;
    console.log(fromdate);
    console.log(todate);
    if (fromdate != "" && todate != ""){
        $.ajax({
            method: "GET",
            url: "/api/searchbydate/",
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
        url: "/api/searchbyname/",
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

function SearchByGender(data){
    $.ajax({
        method: "GET",
        url: "/api/searchbygender/",
        data: { "searchbygender": data.value , "searchbytype": document.getElementById('searchbytype').value },
        success: function (data) {
            update_table(data)
        
        },
        error: function () {
            console.log("error on get search by ")


}   });
};




function update_table(data) {
    console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
       if (elem['active_fee_id']['status'] == 'Paid'){
        row =

        '<tr class="border-2 hover:bg-slate-300">' +
            '<td class="p-2">' +
                '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" onc>' +
            '</td>' +
            '<td class="p-2">'+ elem['member_serial_no'] +'</td>'+
            '<td class="p-2"><div class="flex items-center text-sm">'+
                    '<div class="relative hidden w-8 h-8 mr-3 rounded-full md:block">'+
                        '<img class="object-cover w-full h-full rounded-full"'+ 
                           ' src="'+ elem['member_image'] +'"'+
                            'alt="" loading="lazy" />'+
                        '<div class="absolute inset-0 rounded-full shadow-inner"'+
                            'aria-hidden="true"></div>'+
                    '</div>'+
                    '<div>'+
                        '<p class="font-semibold">'+ elem['member_name'] +'</p>'+
                        '<p class="text-sm text-gray-600 ">'+elem['member_membership_id']['category_name']+'</p>'+
                    '</div>'+
                '</div>'+
            '</td>'+
            '<td class="p-2">'+elem['member_card_id']+'</td>'+
            '<td class="p-2">'+elem['member_contact']+'</td>'+
            '<td class="p-2">'+elem['member_membership_id']['category_months']+'</td>'+
            '<td class="p-2">'+'Masho'+'</td>'+
            '<td class="p-2">'+ elem['member_membership_start_date'] +'</td>'+
            '<td class="p-2">'+elem['member_membership_expiry_date']+'</td>'+
            '<td class="p-2">'+
                '<span class="px-2 py-1 font-semibold leading-tight text-black bg-blue-400 rounded-full">'+ elem['active_fee_id']['status']+ '</span>'+
            '</td>'+
            
            '<td class="p-2" >'+
                '<div class="float-right mr-5">'+
                    '<a href="/memberDetails/?data='+elem['id']+'">'+
                        '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"'+
                            'fill="none" viewBox="0 0 24 24" stroke="currentColor" >'+
                            '<path stroke-linecap="round" stroke-linejoin="round"'+
                                'stroke-width="2"'+
                                'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                        '</svg>'+
                    '</a>'+
                '</div>'+
            '</td>'+
            
            '<td class="p-2">'+
            '<button @click="openSMSModal('+elem['id']+');"'+
                    'class="bg-green-500 drop-shadow-md px-5 rounded-lg rounded-br-none">SMS</button>'+
            '</td>'+
        '</tr>';

       }
       else if (elem['active_fee_id']['status'] == 'Unpaid')  {
        row =

        '<tr class="border-2 hover:bg-slate-300">' +
            '<td class="p-2">' +
                '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" onc>' +
            '</td>' +
            '<td class="p-2">'+ elem['member_serial_no'] +'</td>'+
            '<td class="p-2"><div class="flex items-center text-sm">'+
                    '<div class="relative hidden w-8 h-8 mr-3 rounded-full md:block">'+
                        '<img class="object-cover w-full h-full rounded-full"'+ 
                           ' src="'+ elem['member_image'] +'"'+
                            'alt="" loading="lazy" />'+
                        '<div class="absolute inset-0 rounded-full shadow-inner"'+
                            'aria-hidden="true"></div>'+
                    '</div>'+
                    '<div>'+
                        '<p class="font-semibold">'+ elem['member_name'] +'</p>'+
                        '<p class="text-sm text-gray-600 ">'+elem['member_membership_id']['category_name']+'</p>'+
                    '</div>'+
                '</div>'+
            '</td>'+
            '<td class="p-2">'+elem['member_card_id']+'</td>'+
            '<td class="p-2">'+elem['member_contact']+'</td>'+
            '<td class="p-2">'+elem['member_membership_id']['category_months']+'</td>'+
            '<td class="p-2">'+'Masho'+'</td>'+
            '<td class="p-2">'+ elem['member_membership_start_date'] +'</td>'+
            '<td class="p-2">'+elem['member_membership_expiry_date']+'</td>'+
            '<td class="p-2">'+
                '<span class="px-2 py-1 font-semibold leading-tight text-black bg-yellow-300 rounded-full">'+ elem['active_fee_id']['status']+ '</span>'+
            '</td>'+
            
            '<td class="p-2" >'+
                '<div class="float-right mr-5">'+
                    '<a href="/memberDetails/?data='+elem['id']+'">'+
                        '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"'+
                            'fill="none" viewBox="0 0 24 24" stroke="currentColor" >'+
                            '<path stroke-linecap="round" stroke-linejoin="round"'+
                                'stroke-width="2"'+
                                'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                        '</svg>'+
                    '</a>'+
                '</div>'+
            '</td>'+
            
            '<td class="p-2">'+
            '<button @click="openSMSModal('+elem['id']+');"'+
                    'class="bg-green-500 drop-shadow-md px-5 rounded-lg rounded-br-none">SMS</button>'+
            '</td>'+
        '</tr>';


       }
       else{
        row =

        '<tr class="border-2 hover:bg-slate-300">' +
            '<td class="p-2">' +
                '<input onclick="requestDelete(this)" data-id="' + elem['id'] +'" type="checkbox" class="cursor-pointer rounded-md" onc>' +
            '</td>' +
            '<td class="p-2">'+ elem['member_serial_no'] +'</td>'+
            '<td class="p-2"><div class="flex items-center text-sm">'+
                    '<div class="relative hidden w-8 h-8 mr-3 rounded-full md:block">'+
                        '<img class="object-cover w-full h-full rounded-full"'+ 
                           ' src="'+ elem['member_image'] +'"'+
                            'alt="" loading="lazy" />'+
                        '<div class="absolute inset-0 rounded-full shadow-inner"'+
                            'aria-hidden="true"></div>'+
                    '</div>'+
                    '<div>'+
                        '<p class="font-semibold">'+ elem['member_name'] +'</p>'+
                        '<p class="text-sm text-gray-600 ">'+elem['member_membership_id']['category_name']+'</p>'+
                    '</div>'+
                '</div>'+
            '</td>'+
            '<td class="p-2">'+elem['member_card_id']+'</td>'+
            '<td class="p-2">'+elem['member_contact']+'</td>'+
            '<td class="p-2">'+elem['member_membership_id']['category_months']+'</td>'+
            '<td class="p-2">'+'Masho'+'</td>'+
            '<td class="p-2">'+ elem['member_membership_start_date'] +'</td>'+
            '<td class="p-2">'+elem['member_membership_expiry_date']+'</td>'+
            '<td class="p-2">'+
                '<span class="px-2 py-1 font-semibold leading-tight text-black bg-red-400 rounded-full">'+ elem['active_fee_id']['status']+ '</span>'+
            '</td>'+
            
            '<td class="p-2" >'+
                '<div class="float-right mr-5">'+
                    '<a href="/memberDetails/?data='+elem['id']+'">'+
                        '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer"'+
                            'fill="none" viewBox="0 0 24 24" stroke="currentColor" >'+
                            '<path stroke-linecap="round" stroke-linejoin="round"'+
                                'stroke-width="2"'+
                                'd="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />'+
                        '</svg>'+
                    '</a>'+
                '</div>'+
            '</td>'+
            
            '<td class="p-2">'+
                '<button @click="openSMSModal('+elem['id']+');"'+
                    'class="bg-green-500 drop-shadow-md px-5 rounded-lg rounded-br-none">SMS</button>'+
            '</td>'+
        '</tr>';


       }
        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows);
}


$(document).ready(function() {
    // messages timeout for 10 sec 
    setTimeout(function() {
        $('.message').fadeOut('slow');
    }, 4000); // <-- time in milliseconds, 1000 =  1 sec

    // delete message
    $('body').on('click','.del-msg',function(){
        $('.del-msg').parent().attr('style', 'display:none;');
    })
});
function getNumberOfDays(end) {
    const date1 = new Date();
    const date2 = new Date(end);

    // One day in milliseconds
    const oneDay = 1000 * 60 * 60 * 24;

    // Calculating the time difference between two dates
    const diffInTime = date2.getTime() - date1.getTime();

    // Calculating the no. of days between two dates
    const diffInDays = Math.round(diffInTime / oneDay);
    if (diffInDays+1 == 0) {
        return "Expired";
    }
    else{
        return diffInDays+1;
    }
    // return diffInDays;

}


function get_all_member_remaining_expiredays(){
    console.log('get_all_member_remaining_expiredays');
    $.ajax({
        method: "GET",
        url: "/api/getExpireRemainingDays/",
        success: function (data) {
            
            Object.keys(data).forEach(key => {
                elem = data[key];
                console.log(elem);
                day=getNumberOfDays(elem['member_membership_expiry_date']);
                row=
                '<li class="flex">'+
                '<a class="inline-flex items-center justify-between w-full px-2 py-1 text-sm font-semibold transition-colors duration-150 rounded-md hover:bg-gray-100 hover:text-gray-800  "'+
                    'href="#">'+
                    '<span>'+elem['member_name']+'</span>'+
                    '<span'+
                        'class="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-600 bg-red-100 rounded-full ">'+
                        day
                    '</span>'+
                '</a>'+
                '</li>'
                // all_rows = all_rows + row;
                $('#notifications-menu-expiry-days').append(row);
            });
            // $('#myTable tbody').html(all_rows);
        
        },
        error: function () {
            console.log("error on get search by name");
        }
    });



};

function serialNoCheck(data){
    data=data.value
    $.ajax({
        method: "GET",
        data: {'serial_no':data},
        url: "/api/checkSerialNo/",
        success: function (data) {
            if(data['status']=='success'){
                $('#serial-no').removeClass('text-red-500');
                $('#serial-no').addClass('text-green-500');
                $('#serial-no').text('Available');
            }else{
                $('#serial-no').removeClass('text-green-500');
                $('#serial-no').addClass('text-red-500');
                $('#serial-no').text('Not Available');
            }
        }




    })
}


function SMSModuleChange(data){
    let sms_module=data.value
    $.ajax({
        method: "GET",
        url: "/api/smsForsearch/",
        data:{
            "module":sms_module,
        },
        success: function (data) {
            Object.keys(data).forEach(key => {
                var value = data[key];
                var o = new Option(value['smsFor'], value['smsFor']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(value['smsFor']);
                $("#model-smsfor").append(o);
                

            });
        },
        error: function () {
            console.log("error on get Membership Category months");
        }
    });
}
function AllSMSModuleChange(data){
    let sms_module=data.value
    $.ajax({
        method: "GET",
        url: "/api/smsForsearch/",
        data:{
            "module":sms_module,
        },
        success: function (data) {
            Object.keys(data).forEach(key => {
                var value = data[key];
                var o = new Option(value['smsFor'], value['smsFor']);
                /// jquerify the DOM object 'o' so we can use the html method
                $(o).html(value['smsFor']);
                $("#model-smsfor-all").append(o);
                

            });
        },
        error: function () {
            console.log("error on get Membership Category months");
        }
    });
}

function SmsForChange(data){
    $.ajax({
        method: "GET",
        url: "/api/searchMessage/",
        data:{
            "module":document.getElementById("model-smsModule").value,
            "sms":data.value,
        },
        success: function (data) {
            Object.keys(data).forEach(key => {
                var value = data[key];
                $('#model-smstext').text(value['smsText']);
                

            });
        },
        error: function () {
            console.log("error on get Membership Category months");
        }
    });
}
function AllSmsForChange(data){
    $.ajax({
        method: "GET",
        url: "/api/searchMessage/",
        data:{
            "module":document.getElementById("model-smsModule-all").value,
            "sms":data.value,
        },
        success: function (data) {
            Object.keys(data).forEach(key => {
                var value = data[key];
                $('#model-smstext-all').text(value['smsText']);
                

            });
        },
        error: function () {
            console.log("error on get Membership Category months");
        }
    });
}
function set_member_id(id){
    console.log(id);
    $('#model-member-id').val(id);
}       