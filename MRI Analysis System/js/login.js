const form = document.getElementById("loginForm");

form.addEventListener("submit", function(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Basic empty field check
  if (!email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  // Email format validation
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Hardcoded test credentials (for demo)
  const testUser = {
    email: "test@gmail.com",
    password: "12345"
  };

  if (email === testUser.email && password === testUser.password) {
    alert("Login successful! Redirecting...");
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid credentials. Please try again.");
  }
});
