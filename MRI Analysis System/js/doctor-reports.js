document.addEventListener("DOMContentLoaded", () => {
    const reportsList = document.getElementById("reports-list");

    // Sample report data
    const reports = [
        { id: "R1001", patient: "Sarah Mohamed", date: "25/09/2025" },
        { id: "R1002", patient: "Ahmad Ali", date: "24/09/2025" },
        { id: "R1003", patient: "Lee Jon", date: "23/09/2025" },
        { id: "R1004", patient: "Lena Hosam", date: "22/09/2025" }
    ];

    // Populate reports list
    reports.forEach(report => {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = `report-detail.html?id=${report.id}`;
        link.textContent = `${report.id} - ${report.patient} (${report.date})`;
        li.appendChild(link);
        reportsList.appendChild(li);
    });
});
