document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("upload-form");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const patientId = document.getElementById("patient-id").value.trim();
        const fileInput = document.getElementById("mri-file");
        const file = fileInput.files[0];

        if (!patientId) {
            messageDiv.textContent = "⚠️ Please enter a patient ID.";
            messageDiv.style.color = "#ff4d4d";
            return;
        }

        if (!file) {
            messageDiv.textContent = "⚠️ Please select a file to upload.";
            messageDiv.style.color = "#ff4d4d";
            return;
        }

        // Simulated success
        messageDiv.textContent = `✅ MRI file "${file.name}" uploaded successfully for Patient ${patientId}.`;
        messageDiv.style.color = "#00ff99";

        // Reset form after success
        form.reset();
    });
});
