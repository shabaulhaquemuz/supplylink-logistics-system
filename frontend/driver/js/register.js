const form = document.getElementById("registerForm");
const errorBox = document.getElementById("errorBox");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.style.display = "none";

    const full_name = document.getElementById("full_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value.trim();

    const payload = {
        full_name,
        email,
        phone,
        password
    };

    try {
        const res = await fetch("http://127.0.0.1:8002/api/driver/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            errorBox.innerText = err.detail || "Registration failed";
            errorBox.style.display = "block";
            return;
        }

        // Success — redirect to login page
        alert("Account created successfully! Please login.");
        window.location.href = "index.html";

    } catch (error) {
        errorBox.innerText = "Network error. Please try again.";
        errorBox.style.display = "block";
    }
});
