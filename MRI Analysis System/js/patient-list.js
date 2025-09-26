// ==============================
// Sample Patient Data
// ==============================
const patients = [
  { id: "100001", name: "Sarah Mohamed", age: 30, gender: "Female", condition: "Brain Tumor" },
  { id: "100002", name: "Ahmad Ali", age: 45, gender: "Male", condition: "Migraine" },
  { id: "100003", name: "Lee Jon", age: 28, gender: "Male", condition: "Epilepsy" },
  { id: "100004", name: "Lena Hosam", age: 35, gender: "Female", condition: "Stroke" }
];

// ==============================
// Function to Display Patients
// ==============================
function displayPatients(patientArray) {
  const patientList = document.getElementById("patients");
  patientList.innerHTML = "";

  if (patientArray.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No patients found";
    li.style.padding = "15px";
    li.style.color = "#ffcccc";
    patientList.appendChild(li);
    return;
  }

  patientArray.forEach(patient => {
    const li = document.createElement("li");

    const link = document.createElement("a");
    link.href = `patient-info.html?id=${patient.id}`;
    link.textContent = `${patient.id} - ${patient.name}`;

    li.appendChild(link);
    patientList.appendChild(li);
  });
}

// ==============================
// Initial Display
// ==============================
displayPatients(patients);

// ==============================
// Search Functionality
// ==============================
const searchInput = document.getElementById("patient-search");
const searchButton = document.getElementById("search-button");

const filterPatients = () => {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = patients.filter(
    p =>
      p.id.toLowerCase().includes(query) ||
      p.name.toLowerCase().includes(query)
  );
  displayPatients(filtered);
};

searchButton.addEventListener("click", filterPatients);
searchInput.addEventListener("keypress", e => {
  if (e.key === "Enter") filterPatients();
});
