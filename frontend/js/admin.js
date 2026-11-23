// Hosted backend and frontend use the same domain
const API = "";

const user = JSON.parse(localStorage.getItem("user") || "null");

// Admin login verification
if (!user || user.role !== "admin") {
    window.location.href = "login.html";
}


// Helper function to handle API responses
async function getResponseData(response) {
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
    }

    return data;
}


// Load Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API}/dashboard`);
        const data = await getResponseData(response);

        document.getElementById("totalJobs").textContent = data.total_jobs;
        document.getElementById("pendingJobs").textContent = data.pending;
        document.getElementById("progressJobs").textContent = data.in_progress;
        document.getElementById("readyJobs").textContent = data.ready;

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}


// Load All Job Cards
async function loadJobs() {
    try {
        const response = await fetch(`${API}/jobs`);
        const jobs = await getResponseData(response);

        const table = document.getElementById("jobsTable");

        table.replaceChildren();

        jobs.forEach(job => {
            const row = document.createElement("tr");

            const values = [
                job.id,
                job.customer_name,
                `${job.vehicle_number} - ${job.vehicle_model}`,
                job.job_code
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "";
                row.appendChild(cell);
            });

            // Status
            const statusCell = document.createElement("td");

            const status = document.createElement("span");
            status.textContent = job.status;

            statusCell.appendChild(status);
            row.appendChild(statusCell);

            // Update Status Dropdown
            const actionCell = document.createElement("td");
            const select = document.createElement("select");

            ["Pending", "In Progress", "Ready", "Completed"].forEach(value => {
                const option = document.createElement("option");

                option.value = value;
                option.textContent = value;

                if (job.status === value) {
                    option.selected = true;
                }

                select.appendChild(option);
            });

            select.addEventListener("change", () => {
                updateStatus(job.id, select.value);
            });

            actionCell.appendChild(select);
            row.appendChild(actionCell);

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Job loading error:", error);
    }
}


// Update Job Status
async function updateStatus(id, status) {
    try {
        const response = await fetch(`${API}/jobs/${id}/status`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ status })
        });

        await getResponseData(response);

        await loadDashboard();
        await loadJobs();

    } catch (error) {
        alert(error.message);
    }
}


// Create New Job Card
document.getElementById("jobForm").addEventListener("submit", async (e) => {

    e.preventDefault();

    const job = {
        customer_name: document.getElementById("customerName").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        vehicle_number: document.getElementById("vehicleNumber").value.trim(),
        vehicle_model: document.getElementById("vehicleModel").value.trim(),
        complaint: document.getElementById("complaint").value.trim()
    };

    const message = document.getElementById("jobMessage");
    const button = document.querySelector("#jobForm button[type='submit']");

    message.textContent = "Creating job card...";
    message.style.color = "#526B56";

    if (button) {
        button.disabled = true;
        button.textContent = "Creating...";
    }

    try {
        const response = await fetch(`${API}/jobs`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(job)
        });

        const data = await getResponseData(response);

        message.style.color = "#526B56";

        message.textContent =
            `Job card #${data.job_id} created successfully! Job Code: ${data.job_code}. Estimated Ready: ${data.estimated_ready_time}`;

        document.getElementById("jobForm").reset();

        await loadJobs();
        await loadDashboard();

    } catch (error) {

        console.error("Create Job Error:", error);

        message.style.color = "#D97969";
        message.textContent = error.message;

    } finally {

        if (button) {
            button.disabled = false;
            button.textContent = "+ Create Job Card";
        }
    }
});


// Initial Loading
loadDashboard();
loadJobs();


// Refresh Dashboard Every 15 Seconds
setInterval(() => {
    loadDashboard();
    loadJobs();
}, 15000);