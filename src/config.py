import os

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

# Load non-secret configuration from .env if available.
#
# IMPORTANT:
# No OpenAI API key is loaded or stored here.
# The API key is supplied by the user at runtime through
# the Streamlit interface.
load_dotenv()


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

# Model can be configured through the environment.
# No API key is stored here.
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)


# ============================================================
# STREAMLIT FORM OPTIONS
# ============================================================

GENDER_OPTIONS = [
    "Male",
    "Female",
    "Other",
    "Prefer not to say",
]


DURATION_OPTIONS = [
    "Less than 24 hours",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks",
    "Unknown",
]


LANGUAGE_OPTIONS = [
    "English",
    "Urdu",
]


SYMPTOM_OPTIONS = [
    "Fever",
    "Cough",
    "Sore throat",
    "Runny nose",
    "Headache",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Stomach pain",
    "Back pain",
    "Dizziness",
    "Body aches",
    "Shortness of breath",
    "Chest pain",
    "Other",
]


# ============================================================
# URGENCY LEVELS
# ============================================================

URGENCY_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
    "EMERGENCY",
]


# ============================================================
# MEDICAL DISCLAIMER
# ============================================================

MEDICAL_DISCLAIMER = """
⚠️ **Medical Safety Disclaimer**

MediGuide AI is an educational AI prototype, not a doctor
or medical device.

It does not provide confirmed diagnoses or replace
professional medical advice.

If symptoms are severe, rapidly worsening, or potentially
life-threatening, seek appropriate emergency medical help
immediately.
"""