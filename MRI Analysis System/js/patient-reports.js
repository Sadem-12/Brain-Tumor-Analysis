document.addEventListener("DOMContentLoaded", () => {
    const reportsList = document.getElementById("reports-list");

    // Sample patient-specific reports
    const patientReports = [
        { id: "R1001", doctor: "Dr. Ahmad Ali", date: "25/09/2025" },
        { id: "R1005", doctor: "Dr. Lena Hosam", date: "20/09/2025" },
        { id: "R1008", doctor: "Dr. Lee Jon", date: "15/09/2025" }
    ];

    // Populate reports list
    patientReports.forEach(report => {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = `report-detail.html?id=${report.id}`;
        link.textContent = `${report.id} - ${report.doctor} (${report.date})`;
        li.appendChild(link);
        reportsList.appendChild(li);
    });
});
