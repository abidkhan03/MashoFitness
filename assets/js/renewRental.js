function getUpdateChagne(data) {
    var end_date = new Date(document.getElementById("rent-pay-date").value);
    console.log(end_date);
    var getmonth = data.value 
    
    getmonth = parseInt(getmonth.replace(/[^\d.]/g, ''));
    end_date.setMonth(end_date.getMonth() + getmonth);
    document.getElementById('rent-end-date').value = end_date.toISOString().slice(0, 10);

    var rent = new Number(document.getElementById("rent-amount").value);
    console.log(rent);

    document.getElementById('total-rent').value = rent * getmonth;
}

function getRenewChagne(data) {
    var end_date = new Date(document.getElementById("renew-start-date").value);
    console.log(end_date);
    var getmonth = data.value 
    
    getmonth = parseInt(getmonth.replace(/[^\d.]/g, ''));
    end_date.setMonth(end_date.getMonth() + getmonth);
    document.getElementById('renew-end-date').value = end_date.toISOString().slice(0, 10);

    var rent = new Number(document.getElementById("renew-rent").value);
    console.log(rent);

    document.getElementById('renew-total').value = rent * getmonth;
}

function checkStatus(data){
    data=data.value
    console.log(data)
    
}
function reloadPage() {
    window.location.reload();
    console.log("reload");
};