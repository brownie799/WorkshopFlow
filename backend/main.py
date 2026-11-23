from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import Optional
import hashlib

from database import get_db, init_db
from models import User, JobCard
from ai_engine import classify_complaint


# ==================================================
# APPLICATION SETUP
# ==================================================

app = FastAPI(
    title="WorkshopFlow API",
    description="Two Wheeler Workshop Management System",
    version="1.0.0"
)

# Initialize database and migrations
init_db()


# ==================================================
# CORS CONFIGURATION
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# ADMIN CREDENTIALS
# ==================================================

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"


# ==================================================
# PASSWORD HASHING
# ==================================================

def hash_password(password: str):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==================================================
# REQUEST MODELS
# ==================================================

class LoginRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: str


class JobRequest(BaseModel):
    customer_name: str
    phone: str
    vehicle_number: str
    vehicle_model: str
    complaint: str


class StatusRequest(BaseModel):
    status: str


# ==================================================
# HOME ROUTE
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to WorkshopFlow API",
        "status": "Running"
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "WorkshopFlow"
    }


# ==================================================
# LOGIN
# CUSTOMER AUTOMATIC REGISTRATION + LOGIN
# ==================================================

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    email = str(data.email).lower().strip()

    # ----------------------------------------------
    # ADMIN LOGIN
    # ----------------------------------------------

    if data.role == "admin":

        if (
            email == ADMIN_EMAIL
            and data.password == ADMIN_PASSWORD
        ):
            return {
                "success": True,
                "message": "Admin login successful",
                "role": "admin"
            }

        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )

    # ----------------------------------------------
    # CUSTOMER LOGIN
    # ----------------------------------------------

    elif data.role == "customer":

        customer = db.query(User).filter(
            func.lower(User.email) == email
        ).first()

        # Existing customer
        if customer:

            if getattr(customer, "role", None) != "customer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid customer account"
                )

            stored_password = getattr(customer, "password", None)
            if stored_password != hash_password(data.password):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect password"
                )

        # New customer: automatic account creation
        else:

            if not data.name or not data.name.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Please enter your full name"
                )

            if not data.phone or not data.phone.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Please enter your phone number"
                )

            if len(data.password) < 6:
                raise HTTPException(
                    status_code=400,
                    detail="Password must contain at least 6 characters"
                )

            customer = User(
                name=data.name.strip(),
                email=email,
                phone=data.phone.strip(),
                password=hash_password(data.password),
                role="customer"
            )

            db.add(customer)
            db.commit()
            db.refresh(customer)

        return {
            "success": True,
            "message": "Customer login successful",
            "role": "customer",
            "name": customer.name,
            "email": customer.email
        }

    raise HTTPException(
        status_code=400,
        detail="Invalid login role"
    )


# ==================================================
# CREATE JOB CARD
# ==================================================

@app.post("/jobs")
def create_job(
    request: JobRequest,
    db: Session = Depends(get_db)
):

    if not request.complaint.strip():
        raise HTTPException(
            status_code=400,
            detail="Complaint is required"
        )

    result = classify_complaint(request.complaint)

    new_job = JobCard(
        customer_name=request.customer_name,
        phone=request.phone,
        vehicle_number=request.vehicle_number.upper().strip(),
        vehicle_model=request.vehicle_model,
        complaint=request.complaint,
        job_code=result["job_code"],
        status="Received",
        estimated_hours=result["estimated_hours"],
        estimated_ready_time=result["estimated_ready_time"]
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job card created successfully",
        "job_id": new_job.id,
        "job_code": new_job.job_code,
        "service": result["service"],
        "estimated_hours": new_job.estimated_hours,
        "estimated_ready_time": new_job.estimated_ready_time
    }


# ==================================================
# GET ALL JOB CARDS
# ==================================================

@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(JobCard).order_by(
        JobCard.id.desc()
    ).all()

    return jobs


# ==================================================
# UPDATE JOB STATUS
# ==================================================

@app.put("/jobs/{job_id}/status")
def update_status(
    job_id: int,
    request: StatusRequest,
    db: Session = Depends(get_db)
):

    job = db.query(JobCard).filter(
        JobCard.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job card not found"
        )

    allowed_statuses = [
        "Received",
        "Inspection",
        "In Progress",
        "Waiting for Parts",
        "Completed",
        "Delivered"
    ]

    if request.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid job status"
        )

    job.status = request.status

    db.commit()
    db.refresh(job)

    return {
        "message": "Job status updated successfully",
        "job_id": job.id,
        "status": job.status
    }


# ==================================================
# CUSTOMER VEHICLE TRACKING
# ==================================================

@app.get("/track/{vehicle_number}")
def track_vehicle(
    vehicle_number: str,
    db: Session = Depends(get_db)
):

    jobs = db.query(JobCard).filter(
        JobCard.vehicle_number == vehicle_number.upper().strip()
    ).order_by(
        JobCard.id.desc()
    ).all()

    if not jobs:
        raise HTTPException(
            status_code=404,
            detail="No service record found for this vehicle"
        )

    return jobs


# ==================================================
# DASHBOARD STATISTICS
# ==================================================

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_jobs = db.query(JobCard).count()

    received = db.query(JobCard).filter(
        JobCard.status == "Received"
    ).count()

    inspection = db.query(JobCard).filter(
        JobCard.status == "Inspection"
    ).count()

    in_progress = db.query(JobCard).filter(
        JobCard.status == "In Progress"
    ).count()

    waiting_parts = db.query(JobCard).filter(
        JobCard.status == "Waiting for Parts"
    ).count()

    completed = db.query(JobCard).filter(
        JobCard.status == "Completed"
    ).count()

    delivered = db.query(JobCard).filter(
        JobCard.status == "Delivered"
    ).count()

    total_customers = db.query(User).filter(
        User.role == "customer"
    ).count()

    return {
        "total_jobs": total_jobs,
        "received": received,
        "inspection": inspection,
        "in_progress": in_progress,
        "waiting_parts": waiting_parts,
        "completed": completed,
        "delivered": delivered,
        "total_customers": total_customers
    }