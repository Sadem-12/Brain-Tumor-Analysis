document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const totalPatientsElement = document.getElementById("total-patients");
    const totalScansElement = document.getElementById("total-scans");
    const recentReportsListElement = document.getElementById("recent-reports-list");

    // Example data
    const EXAMPLE_TOTAL_PATIENTS = 25;
    const EXAMPLE_TOTAL_SCANS = 60;
    const recentReports = ["Patient A", "Patient B", "Patient C"];

    // Update dashboard stats
    const updateStats = () => {
        totalPatientsElement.textContent = EXAMPLE_TOTAL_PATIENTS;
        totalScansElement.textContent = EXAMPLE_TOTAL_SCANS;
    };

    // Populate recent reports dynamically
    const populateRecentReports = () => {
        recentReports.forEach(patient => {
            const listItem = document.createElement("li");
            const link = document.createElement("a");
            link.href = "#"; // Replace with actual report link
            link.textContent = `${patient}'s latest report`;
            listItem.appendChild(link);
            recentReportsListElement.appendChild(listItem);
        });
    };

    // Handle navigation placeholders (optional dynamic logic)
    const navLinks = document.querySelectorAll("nav a");
    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const target = e.target.getAttribute("href");
            if (target === "contact-patient.html") {
                console.log("Navigating to Contact Patient page...");
            }
            if (target === "doctor-profile.html") {
                console.log("Navigating to Doctor Profile page...");
            }
        });
    });

    // Initialize
    updateStats();
    populateRecentReports();
});
