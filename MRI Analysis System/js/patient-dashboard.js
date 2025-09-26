document.addEventListener("DOMContentLoaded", () => {
    const totalReportsElement = document.getElementById("total-reports");
    const recentReportsListElement = document.getElementById("recent-reports-list");

    // Example MRI data
    const allReports = [
        { type: "MRI", name: "Brain MRI Scan 1" },
        { type: "Blood Test", name: "Blood Test 1" },
        { type: "MRI", name: "Spine MRI Scan" },
        { type: "CT", name: "CT Scan 1" }
    ];

    // Filter only MRI scans
    const mriReports = allReports.filter(report => report.type === "MRI");

    // Update dashboard stats
    totalReportsElement.textContent = mriReports.length;

    // Populate recent MRI reports dynamically
    mriReports.forEach(report => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = "#"; // replace with actual MRI report link
        link.textContent = report.name;
        listItem.appendChild(link);
        recentReportsListElement.appendChild(listItem);
    });
});
