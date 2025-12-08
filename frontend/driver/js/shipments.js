// js/shipments.js

const API_BASE = "http://127.0.0.1:8002/api/driver";

const shipmentsList = document.getElementById("shipmentsList");
const emptyMsg = document.getElementById("emptyMsg");

const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "index.html";
}

// Fetch Shipments
async function loadShipments() {
    try {
        const res = await fetch(`${API_BASE}/shipments`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            console.error("Failed to fetch shipments");
            shipmentsList.innerHTML = "<p>Error loading shipments</p>";
            return;
        }

        const shipments = await res.json();

        if (!Array.isArray(shipments) || shipments.length === 0) {
            emptyMsg.style.display = "block";
            return;
        }

        renderShipments(shipments);

    } catch (err) {
        console.error("Network error:", err);
        shipmentsList.innerHTML = "<p>Unable to load shipments.</p>";
    }
}

// Render shipment cards
function renderShipments(list) {
    shipmentsList.innerHTML = "";

    list.forEach((s) => {
        const card = document.createElement("div");
        card.className = "shipment-card";

        const statusKey = (s.status || "").toLowerCase();
        const statusClass = {
            "pending": "badge-pending",
            "assigned": "badge-assigned",
            "picked_up": "badge-assigned",
            "in_transit": "badge-in_transit",
            "out_for_delivery": "badge-out_for_delivery",
            "delivered": "badge-delivered",
            "failed": "badge-failed"
        }[statusKey] || "badge-assigned";

        const codBadge = s.is_cod
            ? `<span class="cod-badge">COD: ₹${s.cod_amount ?? 0}</span>`
            : "";

        const eta = s.estimated_delivery
            ? new Date(s.estimated_delivery).toLocaleString()
            : "N/A";

        card.innerHTML = `
            <div class="shipment-header">
                <div class="shipment-id">
                    #${s.shipment_number} &nbsp; (ID: ${s.id})
                </div>
                <span class="status-badge ${statusClass}">
                    ${(s.status || "").replace(/_/g, " ")}
                </span>
            </div>

            <div class="shipment-body">
                <div class="row">
                    <span class="label">Pickup:</span>
                    <span class="value">${s.pickup_location || "—"}</span>
                </div>

                <div class="row">
                    <span class="label">Destination:</span>
                    <span class="value">${s.delivery_location || "—"}</span>
                </div>

                <div class="row">
                    <span class="label">Type:</span>
                    <span class="value">${s.shipment_type || "domestic"}</span>
                    ${codBadge}
                </div>

                <div class="row">
                    <span class="label">Est. Delivery:</span>
                    <span class="value">${eta}</span>
                </div>
            </div>

            <div class="shipment-footer">
                <button class="btn-view" onclick="openDetails(${s.id})">
                    View Details
                </button>
            </div>
        `;

        shipmentsList.appendChild(card);
    });
}

// Navigate to shipment details
function openDetails(id) {
    localStorage.setItem("selected_shipment_id", id);
    window.location.href = "shipment_details.html";
}

loadShipments();
