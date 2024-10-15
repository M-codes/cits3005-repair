function searchProcedures() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const tableRows = document.querySelectorAll('#procedureTable tbody tr');

    tableRows.forEach(row => {
        const procedureName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        if (procedureName.includes(input)) {
            row.style.display = ''; // Show the row
        } else {
            row.style.display = 'none'; // Hide the row
        }
    });
}

function filterByLetter(letter) {
    const tableRows = document.querySelectorAll('#procedureTable tbody tr');
    tableRows.forEach(row => {
        const itemName = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
        if (itemName.startsWith(letter.toLowerCase())) {
            row.style.display = ''; // Show the row
        } else {
            row.style.display = 'none'; // Hide the row
        }
    });
}

function filterByProcedureCount(range) {
    const tableRows = document.querySelectorAll('#procedureTable tbody tr');
    tableRows.forEach(row => {
        const procedureCount = row.querySelectorAll('td:nth-child(2) ul li').length;

        let showRow = false;

        if (range === '0-5' && procedureCount <= 5) {
            showRow = true;
        } else if (range === '5-10' && procedureCount > 5 && procedureCount < 10) {
            showRow = true;
        } else if (range === '10+' && procedureCount >= 10) {
            showRow = true;
        }

        row.style.display = showRow ? '' : 'none'; // Show or hide the row
    });
}