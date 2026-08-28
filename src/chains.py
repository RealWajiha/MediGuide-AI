from typing import Dict, Generator, Any

from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

from .config import OPENAI_MODEL

from .prompts import (
    assessment_prompt_template,
    assessment_chat_template,
    narrative_chat_template,
    JSON_SCHEMA,
    SYSTEM_PROMPT,
)


# ============================================================
# CREATE LLM
# ============================================================

def create_llm(
    api_key: str,
    temperature: float = 0,
):
    """
    Create and return a ChatOpenAI model using the API key
    supplied at runtime by the user.

    The API key is NOT loaded from config.py or .env.
    """

    if not api_key or not api_key.strip():
        raise ValueError(
            "OpenAI API key is required. "
            "Please enter your own API key."
        )

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temperature,
        api_key=api_key.strip(),
    )


# ============================================================
# LLMChain
# ============================================================

def create_assessment_chain(
    api_key: str,
):
    """
    Create the medical assessment LLMChain.

    The user's API key is supplied at runtime and is not
    persisted by this function.
    """

    llm = create_llm(
        api_key=api_key,
    )

    chain = LLMChain(
        llm=llm,
        prompt=assessment_prompt_template,
        verbose=False,
    )

    return chain


# ============================================================
# RUN ASSESSMENT
# ============================================================

def run_assessment(
    inputs: Dict[str, Any],
    api_key: str,
):
    """
    Run the medical assessment chain.

    Parameters
    ----------
    inputs:
        Patient information and assessment inputs.

    api_key:
        OpenAI API key supplied by the user at runtime.

    Returns
    -------
    str
        Raw model output.
    """

    if not api_key or not api_key.strip():
        raise ValueError(
            "OpenAI API key is required. "
            "Please enter your own API key."
        )

    chain = create_assessment_chain(
        api_key=api_key,
    )

    chain_inputs = {
        "age": inputs["age"],
        "gender": inputs["gender"],
        "symptoms": inputs["symptoms"],
        "duration": inputs["duration"],
        "severity": inputs["severity"],
        "conditions": inputs["conditions"],
        "medications": inputs["medications"],
        "notes": inputs["notes"],
        "language": inputs["language"],
        "json_schema": JSON_SCHEMA,
    }

    result = chain.invoke(
        chain_inputs
    )

    # LLMChain usually returns the model response
    # under the "text" key.
    if isinstance(result, dict):
        return result.get(
            "text",
            str(result),
        )

    return str(result)


# ============================================================
# STREAM NARRATIVE
# ============================================================

def stream_narrative(
    assessment: dict,
    language: str,
    api_key: str,
) -> Generator[str, None, None]:
    """
    Stream a human-readable narrative using llm.stream().

    The OpenAI API key is supplied at runtime by the user.
    """

    if not api_key or not api_key.strip():
        raise ValueError(
            "OpenAI API key is required. "
            "Please enter your own API key."
        )

    llm = create_llm(
        api_key=api_key,
    )

    messages = narrative_chat_template.format_messages(
        assessment=str(assessment),
        language=language,
    )

    for chunk in llm.stream(messages):

        if chunk.content:
            yield chunk.content


# ============================================================
# RAW MESSAGE DEMO
# ============================================================

def message_demo():
    """
    Demonstrates SystemMessage, HumanMessage and AIMessage.
    """

    messages = [
        SystemMessage(
            content=(
                "You are a helpful educational medical assistant. "
                "Never provide a confirmed diagnosis."
            )
        ),

        HumanMessage(
            content="Explain why fever can occur."
        ),

        AIMessage(
            content=(
                "Fever can occur when the body's immune system "
                "responds to an infection or other causes."
            )
        ),
    ]

    return messages


# ============================================================
# CHAT PROMPT DEMO
# ============================================================

def build_chat_messages(
    inputs: Dict[str, Any]
):
    """
    Demonstrates ChatPromptTemplate.format_messages().
    """

    return assessment_chat_template.format_messages(
        age=inputs["age"],
        gender=inputs["gender"],
        symptoms=inputs["symptoms"],
        duration=inputs["duration"],
        severity=inputs["severity"],
        conditions=inputs["conditions"],
        medications=inputs["medications"],
        notes=inputs["notes"],
        language=inputs["language"],
        json_schema=JSON_SCHEMA,
    )