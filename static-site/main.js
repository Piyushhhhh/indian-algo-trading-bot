// Example: Dynamically list available reports (to be generated by Python)
document.addEventListener('DOMContentLoaded', () => {
    // This can be replaced by Python generating a JSON manifest
    const reports = [
        { symbol: 'INFY', plot: 'results/INFY-plot.png', report: 'results/INFY-report.csv' },
        { symbol: 'PAYTM', plot: 'results/PAYTM-plot.png', report: 'results/PAYTM-report.csv' },
        { symbol: 'SBIN', plot: 'results/SBIN-plot.png', report: 'results/SBIN-report.csv' }
    ];
    const list = document.getElementById('reports-list');
    reports.forEach(rep => {
        const a = document.createElement('a');
        a.href = rep.plot;
        a.textContent = rep.symbol + ' Plot';
        a.target = '_blank';
        list.appendChild(a);
        const b = document.createElement('a');
        b.href = rep.report;
        b.textContent = rep.symbol + ' Report';
        b.target = '_blank';
        list.appendChild(b);
    });

    // Example: Load sample CSV as a table (static demo)
    fetch('results/SBIN-report.csv')
        .then(resp => resp.text())
        .then(csv => {
            const rows = csv.split('\n').filter(Boolean).map(r => r.split(','));
            let html = '<table border="1" style="margin-top:1rem;max-width:100%">';
            rows.forEach((row, i) => {
                html += '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>';
            });
            html += '</table>';
            document.getElementById('sample-report-table').innerHTML = html;
        });
});
