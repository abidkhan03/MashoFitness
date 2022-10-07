function generate() {
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
    // doc.text(200, y = y + 30, "TOTAL MARKS OF STUDENTS");
    doc.autoTable({
        html: '#myTable',
        startY: 70,
        theme: 'grid',
        // columnStyles: {
        //     0: {
        //         cellWidth: 100,
        //     },
        //     1: {
        //         cellWidth: 100,
        //     },
        //     2: {
        //         cellWidth: 100,
        //     },
        //     3: {
        //         cellWidth: 100,
        //     }
        // },
        styles: {
            minCellHeight: 40
        }
    })
    doc.save('Marks_Of_Students.pdf');
}