// js/login.js - Login Form Handler & Backend Connection

const API_BASE_URL = "http://127.0.0.1:8002/api/driver";

// If already logged in, redirect to dashboard
(function redirectIfAuthenticated() {
  const token = localStorage.getItem("access_token");
  if (token) {
    window.location.href = "dashboard.html";
  }
})();

// Login Form Handler
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const errorBox = document.getElementById("formError");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.style.display = 'none';
    errorBox.textContent = "";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
      showError("Please enter both email and password.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        let msg = "Login failed. Please check your credentials.";
        try {
          const data = await res.json();
          if (data?.detail) msg = data.detail;
        } catch (_) {}
        showError(msg);
        return;
      }

      const data = await res.json();
      // { access_token, token_type, driver: {...} }

      // 🔥 Standardized keys used by ALL pages
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("driver_info", JSON.stringify(data.driver));

      window.location.href = "dashboard.html";
    } catch (err) {
      console.error(err);
      showError("Unable to connect to server. Please try again.");
    }
  });

  function showError(message) {
    errorBox.textContent = message;
    errorBox.style.display = 'block';
  }

  console.log('✅ Login form handler loaded!');
});