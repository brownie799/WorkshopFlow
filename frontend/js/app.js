const API = "http://127.0.0.1:8000";

let selectedRole = "customer";

const roleButtons = document.querySelectorAll(".role-btn");
const customerFields = document.getElementById("customerFields");
const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");

// Role selection
roleButtons.forEach(button => {

    button.addEventListener("click", () => {

        roleButtons.forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");

        selectedRole = button.dataset.role;

        if (selectedRole === "customer") {
            customerFields.style.display = "block";
        } else {
            customerFields.style.display = "none";
        }

        loginMessage.textContent = "";
    });

});

// Login
loginForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (selectedRole === "customer") {

        if (!name || !phone) {
            loginMessage.textContent =
                "Please enter your name and phone number.";
            return;
        }

    }

    const loginData = {
        name: selectedRole === "customer" ? name : null,
        phone: selectedRole === "customer" ? phone : null,
        email: email,
        password: password,
        role: selectedRole
    };

    try {

        loginMessage.textContent = "Please wait...";

        const response = await fetch(`${API}/login`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(loginData)

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Login failed");
        }

        localStorage.setItem("user", JSON.stringify(result));

        loginMessage.textContent = "Login successful!";

        if (result.role === "admin") {
            window.location.href = "admin.html";
        } else {
            window.location.href = "customer.html";
        }

    } catch (error) {

        loginMessage.textContent = error.message;

    }

});