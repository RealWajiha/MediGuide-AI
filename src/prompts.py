from langchain_classic.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)

from langchain_core.messages import SystemMessage


# ============================================================
# JSON SCHEMA
# ============================================================

JSON_SCHEMA = """
{
  "summary": "",
  "possible_conditions": [
    {
      "name": "",
      "reason": ""
    }
  ],
  "urgency_level": "LOW",
  "recommended_next_steps": [],
  "questions_for_doctor": [],
  "warning_signs": []
}
"""


# ============================================================
# SYSTEM SAFETY PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are MediGuide AI, a safety-focused educational medical
symptom assessment assistant.

IMPORTANT SAFETY RULES:

1. You are NOT a doctor.
2. You must NEVER provide a confirmed diagnosis.
3. Do not claim that the patient definitely has a disease.
4. Possible conditions are for educational information only.
5. Encourage professional medical evaluation when appropriate.
6. If symptoms suggest a potentially serious or life-threatening
   situation, recommend seeking urgent/emergency medical help.
7. Do not provide dangerous treatment instructions.
8. Do not recommend prescription medication changes.
9. Be calm, clear, respectful and easy to understand.
10. Consider the patient's age, symptoms, duration, severity,
    medical conditions and medications.
11. Always follow the requested answer language.
12. Return ONLY valid JSON when asked for structured assessment.

The urgency_level MUST be exactly one of:

LOW
MEDIUM
HIGH
EMERGENCY

Your response must match this exact JSON structure:

{
  "summary": "",
  "possible_conditions": [
    {
      "name": "",
      "reason": ""
    }
  ],
  "urgency_level": "",
  "recommended_next_steps": [],
  "questions_for_doctor": [],
  "warning_signs": []
}
"""


# ============================================================
# PROMPT TEMPLATE
# ============================================================

ASSESSMENT_TEMPLATE = """
Patient Information:

Age:
{age}

Gender:
{gender}

Symptoms:
{symptoms}

Duration:
{duration}

Severity:
{severity}/10

Existing Medical Conditions:
{conditions}

Current Medications:
{medications}

Additional Notes:
{notes}

Answer Language:
{language}

Analyze the information above and provide general educational
guidance.

Return ONLY valid JSON.

Do not include markdown.
Do not include ```json.
Do not include explanations outside JSON.

JSON structure:
{json_schema}
"""


# ============================================================
# PromptTemplate
# ============================================================

assessment_prompt_template = PromptTemplate.from_template(
    template=ASSESSMENT_TEMPLATE
)


# ============================================================
# ChatPromptTemplate
# ============================================================

assessment_chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SYSTEM_PROMPT),

        HumanMessagePromptTemplate.from_template(
            ASSESSMENT_TEMPLATE
        )
    ]
)


# ============================================================
# STREAMING NARRATIVE TEMPLATE
# ============================================================

NARRATIVE_SYSTEM_PROMPT = """
You are MediGuide AI.

Create a short, clear and safety-focused explanation based
ONLY on the provided structured assessment.

Rules:

- Never claim a confirmed diagnosis.
- Clearly say that possible conditions are educational possibilities.
- Explain the urgency level.
- Explain the recommended next steps.
- Mention warning signs.
- If urgency is HIGH or EMERGENCY, clearly emphasize seeking
  urgent medical attention.
- Do not give prescription medication instructions.
- Use the requested language.
- Keep the response understandable for a general user.
"""


NARRATIVE_TEMPLATE = """
Create a human-readable guidance summary from this assessment:

{assessment}

Answer language:
{language}
"""


narrative_chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=NARRATIVE_SYSTEM_PROMPT),

        HumanMessagePromptTemplate.from_template(
            NARRATIVE_TEMPLATE
        )
    ]
)


# ============================================================
# Simple PromptTemplate demo
# ============================================================

def build_simple_prompt(age, gender, symptoms):
    """
    Demonstrates the reusable PromptTemplate concept.
    """

    return assessment_prompt_template.format(
        age=age,
        gender=gender,
        symptoms=symptoms,
        duration="Unknown",
        severity=1,
        conditions="None provided",
        medications="None provided",
        notes="None provided",
        language="English",
        json_schema=JSON_SCHEMA
    )