# 🛵 WorkshopFlow – AI-Powered Two-Wheeler Workshop Management System

### Intelligent Workshop Automation | AI-Based Complaint Classification | Digital Job Card Management

WorkshopFlow is a web-based two-wheeler workshop management platform designed to digitalize and simplify service centre operations. It helps administrators manage customers, vehicle service requests, digital job cards and service progress while providing customers with a convenient vehicle tracking experience.

The system includes an AI-based complaint classification engine that identifies common vehicle problems, generates service job codes and estimates repair duration.

---

## 🚀 Key Features

### 👨‍💼 1. Admin Management
- Separate administrator login.
- View customer service requests.
- Manage digital job cards.
- Update vehicle service status.
- Monitor workshop activities.
- View dashboard statistics.

### 👤 2. Customer Management
- Customer login with automatic account creation for new customers.
- Submit vehicle service complaints.
- Enter vehicle details.
- View job card information.
- Track vehicle service progress.
- Check estimated vehicle delivery time.

### 🤖 3. AI Agent – Intelligent Complaint Processing

The WorkshopFlow AI engine assists workshop operations by automatically processing customer complaints.

**What the AI Agent does:**

| Function | Description |
|---|---|
| Complaint Analysis | Analyzes customer complaint text. |
| Problem Classification | Identifies common vehicle issues. |
| Job Code Generation | Assigns predefined service codes. |
| Time Estimation | Estimates service duration. |
| Job Card Support | Supplies classified information for job card creation. |
| Customer Tracking | Makes service progress available to customers. |

### 🔄 AI Agent Workflow

```text
Customer Complaint
       |
       v
AI Complaint Processing Engine
       |
       v
Keyword-Based Classification
       |
       v
Vehicle Problem Identification
       |
       v
Automatic Job Code Generation
       |
       v
Service Time Estimation
       |
       v
Digital Job Card Creation
       |
       v
Customer Service Tracking
```

---

## 🧠 AI Model and Algorithm Used

**Current Model: Rule-Based Classification (Keyword Matching)**

WorkshopFlow currently uses a Python-based rule engine rather than a trained machine learning model.

**Working approach:**
- Takes customer complaints as text input.
- Searches for predefined keywords.
- Matches the complaint with a vehicle service category.
- Assigns a corresponding job code.
- Returns an estimated service duration.

**Supported service categories:**

| Service Category | Example |
|---|---|
| Brake | Brake not working |
| Engine | Engine noise |
| Oil | Oil change |
| Tyre | Tyre puncture |
| Battery | Battery problem |
| Pickup | Low pickup |

**Why this approach?**
- Simple and lightweight.
- Fast complaint processing.
- Easy to maintain and customize.
- Does not require a training dataset.

**Future AI Enhancements:**
- NLP-based Tamil and English complaint understanding.
- Machine Learning-based complaint classification.
- Predictive vehicle maintenance.
- Intelligent mechanic assignment.
- AI-powered service recommendations.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI Engine | Python Rule-Based Classification |
| API Architecture | REST API |
| Development Environment | Visual Studio Code |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```text
WorkshopFlow/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── ai_engine.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── customer.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── app.js
│       ├── admin.js
│       └── customer.js
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/brownie799/WorkshopFlow.git
```

### 2. Navigate to Project

```bash
cd WorkshopFlow
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Environment

```powershell
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 6. Start Backend

```bash
uvicorn main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

### 7. Start Frontend

Open another terminal:

```bash
cd frontend
python -m http.server 5500
```

Frontend URL: `http://127.0.0.1:5500`

---

## 🔐 Login Details

**Admin Login (Local Development):**
- Email: admin@gmail.com
- Password: admin123

**Customer Login:**
- Enter customer details through the customer login form.
- New customer accounts are created automatically.

*Security note: Replace default credentials and implement secure authentication before production deployment.*

---

## 🎨 UI/UX Highlights

- Modern sage green and cream colour theme.
- Clean and interactive website design.
- Separate admin and customer interfaces.
- Responsive layouts for mobile and desktop.
- Easy-to-use navigation.
- Dashboard statistics and service tracking.

---

## 🔮 Future Enhancements

- Multi-branch workshop management.
- Advanced NLP-based complaint understanding.
- Tamil-English mixed-language processing.
- Machine Learning-based repair predictions.
- Intelligent mechanic allocation.
- WhatsApp notifications.
- PostgreSQL database integration.
- Automated daily business reports.
- Real-time workshop analytics.

---

## 🎯 Project Objective

The primary objective of WorkshopFlow is to transform traditional two-wheeler workshop operations into a digital and intelligent service management system.

By combining web technologies, automated complaint classification and digital service tracking, WorkshopFlow aims to reduce manual work, improve operational efficiency and enhance customer experience.

---

## 👩‍💻 Project Repository

**GitHub:** https://github.com/brownie799/WorkshopFlow

⭐ If you find this project interesting, consider giving the repository a star!
