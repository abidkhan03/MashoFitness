function generate() {
    var fromdate = document.getElementById('from-date').value;
    var todate = document.getElementById('to-date').value;
    console.log(fromdate);
    var doc = new jsPDF('p', 'pt', 'letter');
    var htmlstring = '';
    var tempVarToCheckPageHeight = 0;
    var pageHeight = 0;
    pageHeight = doc.internal.pageSize.height;
    specialElementHandlers = {
        // element with id of "bypass" - jQuery style selector  
        '#bypassme': function (element, renderer) {
            // true = "handled elsewhere, bypass text extraction"  
            return true
        }
    };
    margins = {
        top: 15,
        bottom: 6,
        left: 10,
        right: 10,
        width: 100
    };
    var y = 20;
    doc.setLineWidth(2);
    if (document.getElementById('myTable')) {
        var res = doc.autoTableHtmlToJson(document.getElementById('myTable'));
        doc.autoTable(res.columns, res.data);
    }
    if (document.getElementById('myTable1')) {
        var res1 = doc.autoTableHtmlToJson(document.getElementById('myTable1'));
        doc.autoTable(res1.columns, res1.data);
    }
    // doc.autoTable(res1.columns, res1.data);
    if (document.getElementById('myTable2')) {
        var res2 = doc.autoTableHtmlToJson(document.getElementById('myTable2'));
        doc.autoTable(res2.columns, res2.data);
    }
    // doc.autoTable(res2.columns, res2.data);
    if (document.getElementById('myTable3')) {
        var res3 = doc.autoTableHtmlToJson(document.getElementById('myTable3'));
        doc.autoTable(res3.columns, res3.data);
    }
    // doc.autoTable(res3.columns, res3.data);
    if (document.getElementById('totalTable')) {
        var res4 = doc.autoTableHtmlToJson(document.getElementById('totalTable'));
        doc.autoTable(res4.columns, res4.data, {
            theme: 'grid',

        })
    }
    // doc.autoTable(res4.columns, res4.data);
    // doc.text(200, y = y + 30, "TOTAL MARKS OF STUDENTS");
    // doc.output('dataurlnewwindow');
    // doc.autoTable({
    //     html: '#myTable',
    //     startY: 70,
    //     theme: 'grid',
    //     // columnStyles: {
    //     //     0: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     1: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     2: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     3: {
    //     //         cellWidth: 100,
    //     //     }
    //     // },
    //     styles: {
    //         minCellHeight: 40
    //     }
    // }),
    // doc.autoTable({
    //     html: '#myTable1',
    //     startY: 70,
    //     theme: 'grid',
    //     // columnStyles: {
    //     //     0: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     1: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     2: {
    //     //         cellWidth: 100,
    //     //     },
    //     //     3: {
    //     //         cellWidth: 100,
    //     //     }
    //     // },
    //     styles: {
    //         minCellHeight: 40
    //     }
    // })

    doc.save(fromdate + "__" + todate + '_revenue.pdf');
    // doc.output('dataurlnewwindow');
}