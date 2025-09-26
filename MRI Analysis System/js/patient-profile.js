document.addEventListener("DOMContentLoaded", () => {
    const patientData = {
        patientNumber: "P-20250925",
        name: "Arwa Saeed",
        email: "arwa@example.com",
        mobile: "+966 5XXXXXXXX",
        bloodType: "O+",
        allergies: "None",
        chronicConditions: "None",
        notifications: true
    };

    // Populate basic info
    document.getElementById("patientNumber").innerHTML = `<strong>Patient Number:</strong> ${patientData.patientNumber}`;
    document.getElementById("name").innerHTML = `<strong>Name:</strong> ${patientData.name}`;
    document.getElementById("email").innerHTML = `<strong>Email:</strong> ${patientData.email}`;
    document.getElementById("mobile").innerHTML = `<strong>Mobile:</strong> ${patientData.mobile}`;

    // Populate medical info
    document.getElementById("bloodType").innerHTML = `<strong>Blood Type:</strong> ${patientData.bloodType}`;
    document.getElementById("allergies").innerHTML = `<strong>Allergies:</strong> ${patientData.allergies}`;
    document.getElementById("conditions").innerHTML = `<strong>Chronic Conditions:</strong> ${patientData.chronicConditions}`;

    // Populate account settings
    document.getElementById("notifications").innerHTML = `<strong>Notifications:</strong> ${patientData.notifications ? "Enabled" : "Disabled"} <a href="#" class="edit-link">Edit</a>`;
});
