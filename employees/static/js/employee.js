document.getElementById("dateofbirth").onchange = function () {
    var Bdate = this.value;
    var Bday = +new Date(Bdate);
    document.getElementById('emp-age').value = ~~((Date.now() - Bday) / (31557600000));
}

function EmployeeTypeChecker(data){
    data=data.value;
    if(data=="Other"){
        document.getElementById("User-name-div").style.display="none";
    }
    else{
        document.getElementById("User-name-div").style.display="block";
    }
}