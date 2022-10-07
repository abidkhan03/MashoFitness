function get_Bookings(data){
    $.ajax({
        method: "GET",
        url: "/api/getBookings/",
        data: { "booking_date": data.value },
        success: function (data) {
            console.log("success on search");
            var htmlcontainer = "";
            Object.keys(data).forEach(key => {
            elem = data[key];
            console.log(elem);
            if (elem['status']==false){
                console.log("false");
            htmlcontainer+=

            '<div class="flex flex-row gap-1 border p-1 border-teal-900">'+
            '<span>'+elem['time']+elem['meridiem']+'</span>'+
                    '<input type="checkbox" class="m-1 rounded-md" name="check" onclick="onlyOne(this)" value="'+elem['time']+elem['meridiem']+'" >'+
            '</div>'

            
    }
        else{
            console.log("true");
            htmlcontainer+=
            '<div class="flex flex-row gap-1 border p-1 border-teal-900">'+
            '<span>'+elem['time']+elem['meridiem']+'</span>'+
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
            console.log("error on get search by name");
        }
    });
};



function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
    document.getElementById("book-at").value = checkbox.value;
}

