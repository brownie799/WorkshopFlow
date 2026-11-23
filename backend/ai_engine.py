from datetime import datetime, timedelta


SERVICE_RULES = {
    "brake": {
        "code": "BRK-001",
        "hours": 1.5,
        "service": "Brake Service"
    },

    "engine": {
        "code": "ENG-001",
        "hours": 3.0,
        "service": "Engine Repair"
    },

    "oil": {
        "code": "OIL-001",
        "hours": 0.5,
        "service": "Oil Change"
    },

    "tyre": {
        "code": "TYR-001",
        "hours": 1.0,
        "service": "Tyre Service"
    },

    "tire": {
        "code": "TYR-001",
        "hours": 1.0,
        "service": "Tyre Service"
    },

    "battery": {
        "code": "BAT-001",
        "hours": 1.0,
        "service": "Battery Service"
    },

    "pickup": {
        "code": "PUP-001",
        "hours": 2.0,
        "service": "Pickup Problem"
    }
}


def classify_complaint(complaint):

    complaint_text = complaint.lower()

    for keyword, details in SERVICE_RULES.items():

        if keyword in complaint_text:

            ready_time = datetime.now() + timedelta(
                hours=details["hours"]
            )

            return {
                "job_code": details["code"],
                "service": details["service"],
                "estimated_hours": details["hours"],
                "estimated_ready_time": ready_time
            }

    ready_time = datetime.now() + timedelta(hours=1)

    return {
        "job_code": "GEN-001",
        "service": "General Service",
        "estimated_hours": 1.0,
        "estimated_ready_time": ready_time
    }