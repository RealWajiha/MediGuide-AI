# ============================================================
# MediGuide AI
# API Key Login -> MediGuide Interface
# ============================================================

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide"
)


# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------

if "api_key" not in st.session_state:
    st.session_state.api_key = None


# ============================================================
# API KEY SCREEN
# ============================================================

if not st.session_state.api_key:

    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>🩺 MediGuide AI</h1>
            <p style="font-size:20px; color:gray;">
                AI-Powered Medical Symptom Assessment & Patient Guidance
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Enter OpenAI API Key")

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-..."
        )

        st.caption(
            "Your API key is used only for this session."
        )

        if st.button(
            "Continue →",
            type="primary",
            use_container_width=True
        ):

            if not api_key.strip():

                st.error("Please enter your API key.")

            elif not api_key.startswith("sk-"):

                st.error("Please enter a valid OpenAI API key.")

            else:

                st.session_state.api_key = api_key

                st.rerun()

    st.stop()


# ============================================================
# MEDIGUIDE INTERFACE
# ============================================================

st.title("🩺 MediGuide AI")

st.markdown(
    """
    **AI-Powered Medical Symptom Assessment and Patient Guidance Assistant**
    
    MediGuide AI provides general educational guidance based on the
    information you provide.
    """
)

st.warning(
    "⚠️ MediGuide AI is an educational prototype. "
    "It does not provide a medical diagnosis and should not replace "
    "professional medical advice."
)


# ------------------------------------------------------------
# Create LLM
# ------------------------------------------------------------

try:

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=st.session_state.api_key
    )

except Exception as e:

    st.error("Unable to initialize AI model.")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Patient Information")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=20
    )

    gender = st.selectbox(
        "Gender",
        ["Prefer not to say", "Male", "Female", "Other"]
    )

    st.divider()

    st.subheader("🏥 Medical Context")

    conditions = st.text_area(
        "Existing Conditions",
        placeholder="e.g. Asthma, diabetes..."
    )

    medications = st.text_area(
        "Current Medications",
        placeholder="Enter current medications..."
    )

    notes = st.text_area(
        "Additional Notes",
        placeholder="Any additional information..."
    )

    st.divider()

    if st.button("🔑 Change API Key", use_container_width=True):

        st.session_state.api_key = None
        st.rerun()


# ============================================================
# SYMPTOM INPUT
# ============================================================

st.header("🔍 Symptom Assessment")

symptoms = st.text_area(
    "Describe your symptoms",
    placeholder=(
        "Example: I have headache and mild fever "
        "for the last two days..."
    ),
    height=160
)

col1, col2 = st.columns(2)

with col1:

    duration = st.text_input(
        "⏱️ Duration",
        placeholder="e.g. 2 days, 1 week"
    )

with col2:

    severity = st.select_slider(
        "📊 Severity",
        options=[
            "Very Mild",
            "Mild",
            "Moderate",
            "Severe",
            "Very Severe"
        ],
        value="Mild"
    )


# ============================================================
# ANALYSIS
# ============================================================

if st.button(
    "🩺 Analyze Symptoms",
    type="primary",
    use_container_width=True
):

    if not symptoms.strip():

        st.error("Please enter your symptoms first.")

    else:

        with st.spinner("🔄 Analyzing symptoms..."):

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
                        You are MediGuide AI, a medical guidance
                        assistant.

                        Provide general educational information only.
                        Do not claim to diagnose the patient.

                        Analyze the provided symptoms and give:

                        1. Possible general causes or considerations
                        2. Urgency level: LOW, MEDIUM, HIGH, or EMERGENCY
                        3. Recommended next steps
                        4. Safety warnings
                        5. When professional medical care should be sought

                        Keep the response clear and structured.
                        """
                    ),
                    (
                        "human",
                        """
                        Patient Information:

                        Age: {age}
                        Gender: {gender}

                        Symptoms:
                        {symptoms}

                        Duration:
                        {duration}

                        Severity:
                        {severity}

                        Existing Conditions:
                        {conditions}

                        Current Medications:
                        {medications}

                        Additional Notes:
                        {notes}
                        """
                    )
                ]
            )

            chain = prompt | llm

            try:

                response = chain.invoke(
                    {
                        "age": age,
                        "gender": gender,
                        "symptoms": symptoms,
                        "duration": duration,
                        "severity": severity,
                        "conditions": conditions,
                        "medications": medications,
                        "notes": notes
                    }
                )

                st.success("Assessment completed!")

                st.divider()

                st.header("📋 MediGuide Assessment")

                st.markdown(response.content)

            except Exception as e:

                st.error(
                    "❌ Unable to generate the assessment."
                )

                st.caption(
                    "Please check your API key and try again."
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MediGuide AI | Educational Prototype | "
    "Python • Streamlit • LangChain • OpenAI"
)