import json
import re


# ============================================================
# REMOVE MARKDOWN JSON FENCES
# ============================================================

def clean_json_text(text: str) -> str:
    """
    Remove accidental markdown fences and surrounding whitespace.
    """

    if not text:
        return ""

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove ```
    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ============================================================
# SAFE JSON PARSER
# ============================================================

def safe_json_parse(raw_output: str):
    """
    Safely parse model output as JSON.

    Returns:
        (True, parsed_data, None)

    OR

        (False, None, error_message)
    """

    cleaned = clean_json_text(raw_output)

    try:

        data = json.loads(cleaned)

        if not isinstance(data, dict):
            return (
                False,
                None,
                "The model response is not a JSON object."
            )

        return True, data, None

    except json.JSONDecodeError as error:

        return (
            False,
            None,
            f"Invalid JSON response: {error}"
        )


# ============================================================
# VALIDATE ASSESSMENT
# ============================================================

def validate_assessment(data: dict):
    """
    Make sure required fields exist.
    """

    required_fields = [
        "summary",
        "possible_conditions",
        "urgency_level",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        return False, f"Missing fields: {', '.join(missing)}"

    urgency = str(
        data.get("urgency_level", "")
    ).upper()

    allowed_levels = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "EMERGENCY"
    ]

    if urgency not in allowed_levels:
        data["urgency_level"] = "MEDIUM"
    else:
        data["urgency_level"] = urgency

    # Make sure list fields are lists
    list_fields = [
        "possible_conditions",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs"
    ]

    for field in list_fields:

        if not isinstance(data[field], list):
            data[field] = []

    return True, data


# ============================================================
# FORM VALIDATION
# ============================================================

def validate_patient_input(age, symptoms):
    """
    Validate required patient input.
    """

    if not str(age).strip():
        return False, "Please enter the patient's age."

    if not symptoms.strip():
        return False, "Please enter or select at least one symptom."

    return True, ""


# ============================================================
# SYMPTOM FORMATTER
# ============================================================

def format_symptoms(selected_symptoms, additional_symptoms):
    """
    Combine multiselect symptoms and free-text symptoms.
    """

    symptoms = list(selected_symptoms)

    if additional_symptoms.strip():
        symptoms.append(
            additional_symptoms.strip()
        )

    if not symptoms:
        return ""

    return ", ".join(symptoms)


# ============================================================
# URGENCY DESCRIPTION
# ============================================================

def urgency_description(level):
    """
    Return a user-friendly urgency explanation.
    """

    descriptions = {

        "LOW":
            "Symptoms appear lower urgency based on the provided information. "
            "Continue monitoring and consider routine professional advice if needed.",

        "MEDIUM":
            "Consider contacting a healthcare professional, especially if symptoms "
            "persist, worsen, or new symptoms appear.",

        "HIGH":
            "Prompt medical evaluation is recommended. Seek professional medical "
            "attention as soon as reasonably possible.",

        "EMERGENCY":
            "Seek emergency medical help immediately. Do not rely on this AI system "
            "for an emergency situation."
    }

    return descriptions.get(
        str(level).upper(),
        descriptions["MEDIUM"]
    )