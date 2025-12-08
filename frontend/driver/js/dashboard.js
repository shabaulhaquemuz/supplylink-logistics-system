// js/dashboard.js

const API_BASE = "http://127.0.0.1:8002/api/driver";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    // Driver name
    const driverInfoRaw = localStorage.getItem("driver_info");
    if (driverInfoRaw) {
        try {
            const driverInfo = JSON.parse(driverInfoRaw);
            document.getElementById("driverName").textContent =
                driverInfo.full_name || "Driver";
        } catch (e) {
            document.getElementById("driverName").textContent = "Driver";
        }
    }

    loadDashboardData(token);

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("driver_info");
            window.location.href = "index.html";
        });
    }
});

async function loadDashboardData(token) {
    try {
        const res = await fetch(`${API_BASE}/dashboard`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            console.log("Error loading dashboard");
            return;
        }

        const data = await res.json();

        // Metrics
        document.getElementById("metricDeliveries").textContent =
            data.total_deliveries_today;
        document.getElementById("metricPending").textContent =
            data.pending_shipments;
        document.getElementById("metricCompleted").textContent =
            data.completed_shipments;
        document.getElementById("metricFailed").textContent =
            data.failed_shipments;

        // Current Shipment
        const box = document.getElementById("currentShipmentBox");
        if (data.current_shipment) {
            box.innerHTML = `
                <div class="ship-info">
                    <p><strong>ID:</strong> ${data.current_shipment.id}</p>
                    <p><strong>Shipment Number:</strong> ${data.current_shipment.shipment_number}</p>
                    <p><strong>Pickup:</strong> ${data.current_shipment.pickup_location}</p>
                    <p><strong>Delivery:</strong> ${data.current_shipment.delivery_location}</p>
                    <p><strong>Status:</strong> ${data.current_shipment.status}</p>
                </div>
            `;
        } else {
            box.innerHTML = "<p>No active shipment.</p>";
        }

        // Last Known Location
        const loc = document.getElementById("locationBox");
        if (data.last_known_location) {
            loc.innerHTML = `
                <p><strong>Latitude:</strong> ${data.last_known_location.latitude}</p>
                <p><strong>Longitude:</strong> ${data.last_known_location.longitude}</p>
                <p><strong>Location:</strong> ${data.last_known_location.location_name}</p>
                <p><strong>Time:</strong> ${new Date(
                    data.last_known_location.timestamp
                ).toLocaleString()}</p>
            `;
        } else {
            loc.innerHTML = "<p>No location updates yet.</p>";
        }
    } catch (err) {
        console.error("Dashboard load error:", err);
    }
}
