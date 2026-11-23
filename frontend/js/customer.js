const API = "";

const user = JSON.parse(localStorage.getItem("user") || "null");

if (!user || user.role !== "customer") {
    window.location.href = "login.html";
}


document.getElementById("trackForm").addEventListener("submit", async (e) => {

    e.preventDefault();

    const vehicleNumber = document.getElementById("trackNumber").value.trim();

    const result = document.getElementById("trackingResult");

    result.textContent = "Searching for your vehicle...";

    try {

        const response = await fetch(
            `${API}/track/${encodeURIComponent(vehicleNumber)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Vehicle not found");
        }


        const card = document.createElement("div");
        card.className = "tracking-result-card";


        const heading = document.createElement("h3");
        heading.textContent = "Vehicle Service Details";

        card.appendChild(heading);


        const details = [
            ["Customer", data.customer_name],
            ["Vehicle Number", data.vehicle_number],
            ["Vehicle Model", data.vehicle_model],
            ["Complaint", data.complaint],
            ["Job Code", data.job_code],
            ["Estimated Ready Time", data.estimated_ready_time]
        ];


        details.forEach(([label, value]) => {

            const paragraph = document.createElement("p");

            const strong = document.createElement("strong");
            strong.textContent = `${label}: `;

            paragraph.appendChild(strong);
            paragraph.appendChild(document.createTextNode(value));

            card.appendChild(paragraph);

        });


        const status = document.createElement("div");

        status.className = "tracking-status";
        status.textContent = `Current Status: ${data.status}`;

        card.appendChild(status);


        result.replaceChildren(card);

    }

    catch (error) {

        result.textContent = error.message;
        result.style.color = "#D97969";

    }

});


function logout() {

    localStorage.removeItem("user");

    window.location.href = "login.html";

}