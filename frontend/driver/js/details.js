// js/details.js

const API_BASE = "http://127.0.0.1:8002/api/driver";

const token = localStorage.getItem("access_token");
if (!token) {
    window.location.href = "index.html";
}

const shipmentId = localStorage.getItem("selected_shipment_id");
if (!shipmentId) {
    window.location.href = "shipments.html";
}

// DOM elements
const shipIdEl = document.getElementById("shipId");
const custNameEl = document.getElementById("custName");
const custPhoneEl = document.getElementById("custPhone");
const pkgWeightEl = document.getElementById("pkgWeight");
const pkgTypeEl = document.getElementById("pkgType");
const pickupAddrEl = document.getElementById("pickupAddr");
const deliveryAddrEl = document.getElementById("deliveryAddr");
const statusBadgeEl = document.getElementById("statusBadge");
const codBoxEl = document.getElementById("codBox");
const timelineEl = document.getElementById("timeline");

// Load details
async function loadShipmentDetails() {
    try {
        const res = await fetch(`${API_BASE}/shipments/${shipmentId}`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!res.ok) {
            alert("Failed to load shipment details.");
            return;
        }

        const s = await res.json();
        renderShipmentDetails(s);
    } catch (err) {
        console.error("Error loading shipment:", err);
        alert("Network error.");
    }
}

function renderShipmentDetails(s) {
    shipIdEl.textContent = s.id;

    custNameEl.textContent = s.customer_name ?? "—";
    custPhoneEl.textContent = s.customer_phone ?? "—";

    pkgWeightEl.textContent = `${s.weight} kg`;
    pkgTypeEl.textContent = s.cargo_type || "Standard";

    pickupAddrEl.textContent = s.pickup_location || "—";
    deliveryAddrEl.textContent = s.delivery_location || "—";

    renderStatusBadge(s.status);
    renderCOD(s);
    renderTimeline(s.tracking_history || []); // will show "No tracking" if empty
}

function renderStatusBadge(status) {
    const key = (status || "").toLowerCase();
    const cls = {
        pending: "badge-pending",
        assigned: "badge-assigned",
        picked_up: "badge-assigned",
        in_transit: "badge-in_transit",
        out_for_delivery: "badge-out_for_delivery",
        delivered: "badge-delivered",
        failed: "badge-failed",
    }[key] || "badge-assigned";

    statusBadgeEl.innerHTML = `
        <span class="status-badge ${cls}">
            ${(status || "").replace(/_/g, " ")}
        </span>
    `;
}

function renderCOD(s) {
    if (s.is_cod) {
        codBoxEl.style.display = "block";
        codBoxEl.innerHTML = `<strong>COD Amount: ₹${s.cod_amount}</strong>`;
    } else {
        codBoxEl.style.display = "none";
    }
}

function renderTimeline(history) {
    if (!history || !history.length) {
        timelineEl.innerHTML = "<p>No tracking updates yet.</p>";
        return;
    }

    timelineEl.innerHTML = history.map(item => `
        <div class="timeline-item">
            <div><strong>${item.status.replace(/_/g, " ")}</strong></div>
            <div>${item.timestamp}</div>
        </div>
    `).join("");
}

// Generic POST helper
async function postAction(endpoint, payload = {}) {
    try {
        const res = await fetch(`${API_BASE}/shipments/${endpoint}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            alert(err.detail || "Action failed.");
            return;
        }

        alert("Action completed successfully!");
        loadShipmentDetails();
    } catch (err) {
        console.error(err);
        alert("Network error.");
    }
}

// Button actions
function markPickedUp() {
    postAction("pickup", {
        shipment_id: Number(shipmentId),
        notes: null
    });
}

function markInTransit() {
    postAction("in-transit", {
        shipment_id: Number(shipmentId),
        notes: null
    });
}

function markOutForDelivery() {
    postAction("out-for-delivery", {
        shipment_id: Number(shipmentId),
        notes: null
    });
}

function markDelivered() {
    postAction("deliver", {
        shipment_id: Number(shipmentId),
        signature: null,
        photo_proof: null,
        notes: null
    });
}

function markFailed() {
    const reasonText = prompt("Enter failure reason (e.g. customer not available, wrong address):");
    if (!reasonText) return;

    // Send enum-friendly reason + keep real text in notes
    postAction("fail", {
        shipment_id: Number(shipmentId),
        failure_reason: "OTHER",   // maps to FailureReason.OTHER
        notes: reasonText
    });
}

function collectCOD() {
    const amount = prompt("Enter COD amount collected:");
    if (!amount || isNaN(amount)) {
        alert("Invalid amount.");
        return;
    }

    postAction("cod-collect", {
        shipment_id: Number(shipmentId),
        amount_collected: Number(amount)
    });
}

function reportDelay() {
    const reasonText = prompt("Enter delay reason (e.g. traffic, breakdown):");
    if (!reasonText) return;

    postAction("report-delay", {
        shipment_id: Number(shipmentId),
        delay_reason: "OTHER",  // maps to DelayReason.OTHER on backend
        notes: reasonText
    });
}

loadShipmentDetails();
