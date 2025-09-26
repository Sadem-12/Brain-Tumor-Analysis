document.getElementById("forgotForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const emailInput = document.getElementById("email");
  const email = emailInput.value.trim();

  if (!email) {
    alert("Please enter your email address.");
    return;
  }

  // Simulate sending reset link
  alert(`A password reset link has been sent to ${email}!`);

  // Reset the form
  emailInput.value = "";
});
