document.addEventListener("DOMContentLoaded", () => {
  const doctorData = {
    doctorId: "D-20250925",
    name: "Dr. Mohammad Ahmed",
    email: "mohammed@example.com",
    mobile: "+966 5XXXXXXXX",
    specialization: "Radiology",
    license: "LIC-987654321",
    experience: "15 years",
    notifications: true
  };

  // Basic Info
  document.getElementById("doctorId").innerHTML = `<strong>Doctor ID:</strong> ${doctorData.doctorId}`;
  document.getElementById("name").innerHTML = `<strong>Name:</strong> ${doctorData.name}`;
  document.getElementById("email").innerHTML = `<strong>Email:</strong> ${doctorData.email}`;
  document.getElementById("mobile").innerHTML = `<strong>Mobile:</strong> ${doctorData.mobile}`;

  // Professional Info
  document.getElementById("specialization").innerHTML = `<strong>Specialization:</strong> ${doctorData.specialization}`;
  document.getElementById("license").innerHTML = `<strong>License Number:</strong> ${doctorData.license}`;
  document.getElementById("experience").innerHTML = `<strong>Experience:</strong> ${doctorData.experience}`;

  // Account Settings
  document.getElementById("notifications").innerHTML =
    `<strong>Notifications:</strong> ${doctorData.notifications ? "Enabled" : "Disabled"} 
     <a href="#" class="edit-link">Edit</a>`;
});
