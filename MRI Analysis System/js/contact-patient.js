document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contactPatientForm");
  const messagesList = document.getElementById("patientMessages");
  let messages = [];

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const patientId = document.getElementById("patientId").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const message = document.getElementById("message").value.trim();

    if (patientId && subject && message) {
      const newMessage = {
        patientId,
        subject,
        message,
        date: new Date().toLocaleString()
      };
      messages.push(newMessage);
      displayMessages();
      form.reset();
    }
  });

  function displayMessages() {
    messagesList.innerHTML = "";
    messages.forEach(msg => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>To Patient ${msg.patientId}</strong> <br>
                      <em>${msg.subject}</em> <br>
                      ${msg.message} <br>
                      <small>${msg.date}</small>`;
      messagesList.appendChild(li);
    });
  }
});
