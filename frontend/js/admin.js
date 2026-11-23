const API = "http://127.0.0.1:8000";

const user = JSON.parse(localStorage.getItem("user") || "null");

if (!user || user.role !== "admin") {
    window.location.href = "login.html";
}


async function loadDashboard() {

    try {

        const response = await fetch(`${API}/dashboard`);

        const data = await response.json();

        document.getElementById("totalJobs").textContent = data.total_jobs;
        document.getElementById("pendingJobs").textContent = data.pending;
        document.getElementById("progressJobs").textContent = data.in_progress;
        document.getElementById("readyJobs").textContent = data.ready;

    }

    catch (error) {
        console.error("Dashboard error:", error);
    }

}


async function loadJobs() {

    try {

        const response = await fetch(`${API}/jobs`);

        const jobs = await response.json();

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
                cell.textContent = value;
                row.appendChild(cell);

            });


            const statusCell = document.createElement("td");

            const status = document.createElement("span");
            status.textContent = job.status;

            statusCell.appendChild(status);
            row.appendChild(statusCell);


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

    }

    catch (error) {
        console.error("Job loading error:", error);
    }

}


async function updateStatus(id, status) {

    try {

        const response = await fetch(`${API}/jobs/${id}/status`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({ status })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to update status");
        }

        await loadDashboard();
        await loadJobs();

    }

    catch (error) {
        alert(error.message);
    }

}


document.getElementById("jobForm").addEventListener("submit", async (e) => {

    e.preventDefault();

    const job = {

        customer_name: document.getElementById("customerName").value,
        phone: document.getElementById("phone").value,
        vehicle_number: document.getElementById("vehicleNumber").value,
        vehicle_model: document.getElementById("vehicleModel").value,
        complaint: document.getElementById("complaint").value

    };


    const message = document.getElementById("jobMessage");

    message.textContent = "Creating job card...";

    try {

        const response = await fetch(`${API}/jobs`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(job)

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to create job");
        }

        message.style.color = "#526B56";

        message.textContent =
            `Job card #${data.job_id} created! Job Code: ${data.job_code}. Estimated Ready: ${data.estimated_ready_time}`;

        document.getElementById("jobForm").reset();

        await loadJobs();
        await loadDashboard();

    }

    catch (error) {

        message.style.color = "#D97969";
        message.textContent = error.message;

    }

});


loadDashboard();
loadJobs();

setInterval(() => {
    loadDashboard();
    loadJobs();
}, 15000);