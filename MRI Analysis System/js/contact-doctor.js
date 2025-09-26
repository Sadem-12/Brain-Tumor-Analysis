document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contactDoctorForm");
  const messagesList = document.getElementById("doctorMessages");
  let messages = [];

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const doctorId = document.getElementById("doctorId").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const message = document.getElementById("message").value.trim();

    if (doctorId && subject && message) {
      const newMessage = {
        doctorId,
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
      li.innerHTML = `<strong>To Doctor ${msg.doctorId}</strong> <br>
                      <em>${msg.subject}</em> <br>
                      ${msg.message} <br>
                      <small>${msg.date}</small>`;
      messagesList.appendChild(li);
    });
  }
});
