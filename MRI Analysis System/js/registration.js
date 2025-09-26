document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get form data
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const mobile = document.getElementById('mobile').value.trim();
    const password = document.getElementById('password').value.trim();
    const role = document.querySelector('input[name="role"]:checked')?.value;

    // Basic empty field check
    if (!fullName || !email || !mobile || !password || !role) {
        alert("Please fill in all fields.");
        return;
    }

    // Email format validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    // Mobile number validation (basic)
    const mobilePattern = /^[0-9]{7,15}$/;
    if (!mobilePattern.test(mobile)) {
        alert("Please enter a valid mobile number (7-15 digits).");
        return;
    }

    // Simulate successful registration
    console.log('Form Data Submitted:', { fullName, email, mobile, password, role });
    alert(`Registration successful for ${fullName} as ${role}!`);

    // Reset the form
    this.reset();
});
