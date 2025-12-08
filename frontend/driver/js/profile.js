// profile.js

document.addEventListener("DOMContentLoaded", () => {

    const token = localStorage.getItem("access_token");
    const driverRaw = localStorage.getItem("driver_info");

    // If not logged in → go back to login
    if (!token || !driverRaw) {
        window.location.href = "index.html";
        return;
    }

    let driver;
    try {
        driver = JSON.parse(driverRaw);
    } catch {
        window.location.href = "index.html";
        return;
    }

    // Fill profile values
    document.getElementById("driverNameTop").textContent = driver.full_name;
    document.getElementById("fullName").textContent = driver.full_name;
    document.getElementById("email").textContent = driver.email;
    document.getElementById("phone").textContent = driver.phone ?? "N/A";
    document.getElementById("driverId").textContent = driver.id;

    // Logout button
    document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("driver_info");
        window.location.href = "index.html";
    });
});

function goDashboard() {
    window.location.href = "dashboard.html";
}
