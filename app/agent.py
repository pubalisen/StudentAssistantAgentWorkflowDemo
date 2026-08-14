"""UCSC Student Services Agent — ADK 2.0 Multi-Agent Workflows + RAG + Grounding.

Demonstrates production-grade ADK 2.0 patterns for a UC Santa Cruz student portal:

  1. SequentialAgent  — Enrollment Pipeline: Prereq Check → Schedule Build → Confirm
  2. ParallelAgent    — Semester Dashboard: Courses + Financial Aid + Housing + Events
  3. LlmAgent         — Academic Advisor: data-backed advising with knowledge tools
  4. LlmAgent         — Web Search: Google Search grounding (isolated from FunctionTools)
  5. FunctionTool     — RAG Knowledge Base: 8 UCSC corpus documents
"""

import pathlib
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.tools import google_search, FunctionTool


# =============================================================================
# CORPUS — Load UCSC knowledge base as tool-callable functions
# =============================================================================

CORPUS_DIR = pathlib.Path(__file__).parent / "corpus"


def _load_corpus(filename: str) -> str:
    """Load a corpus document as a string."""
    path = CORPUS_DIR / filename
    if path.exists():
        return path.read_text()
    return f"[Corpus file {filename} not found]"


# ── Corpus lookup tool — lets agents retrieve specific documents on demand ──

def lookup_ucsc_knowledge(
    topic: str,
) -> str:
    """Look up UCSC knowledge base documents by topic.

    Args:
        topic: The topic to look up. Valid topics are:
            - "cs_requirements" — Computer Science B.S. prerequisites, courses, 4-year plan
            - "bio_requirements" — Biology, MCD Biology, Biochemistry degree requirements
            - "tuition" — Tuition, fees, cost of attendance, financial aid programs
            - "calendar" — Academic calendar, quarter dates, enrollment deadlines
            - "professors" — CSE faculty profiles, office hours, research areas
            - "faq" — Common student questions about enrollment, advising, housing
            - "housing" — Housing rates, meal plans, residential colleges, dining
            - "campus_map" — Building locations, parking, transit routes, walking times

    Returns:
        The full text content of the requested knowledge document.
    """
    topic_to_file = {
        "cs_requirements": "cs-bs-requirements.md",
        "bio_requirements": "biology-biochem-requirements.md",
        "tuition": "tuition-and-fees.md",
        "calendar": "academic-calendar.md",
        "professors": "professors-and-advising.md",
        "faq": "ucsc-faq.md",
        "housing": "housing-and-dining.md",
        "campus_map": "campus-map-and-buildings.md",
    }
    filename = topic_to_file.get(topic)
    if not filename:
        available = ", ".join(topic_to_file.keys())
        return f"Unknown topic '{topic}'. Available topics: {available}"
    return _load_corpus(filename)


knowledge_tool = FunctionTool(func=lookup_ucsc_knowledge)


# =============================================================================
# 1. SEQUENTIAL AGENT — Enrollment Pipeline
# =============================================================================

prereq_check_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="prereq_check_agent",
    description="Validates prerequisites for requested courses.",
    instruction=(
        "You are a UCSC prerequisite validation engine.\n\n"
        "FIRST: Call the lookup_ucsc_knowledge tool with topic='cs_requirements' "
        "to get the prerequisite data.\n\n"
        "Then for each course the student wants:\n"
        "1. Check it against the prerequisite data\n"
        "2. List ALL prerequisites (direct and transitive)\n"
        "3. Mark each as ✅ (assumed completed) or ❓ (unknown)\n"
        "4. Flag any missing prerequisites\n\n"
        "Output a structured prereq report in markdown.\n"
        "Store findings in state key 'prereq_status'."
    ),
    tools=[knowledge_tool],
    output_key="prereq_status",
)

schedule_builder_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="schedule_builder_agent",
    description="Builds a conflict-free course schedule.",
    instruction=(
        "You are a UCSC schedule builder. Read the prereq status from state "
        "key 'prereq_status'.\n\n"
        "Call lookup_ucsc_knowledge with topic='professors' and topic='calendar' "
        "to get professor and scheduling data.\n\n"
        "Then:\n"
        "1. Only schedule courses where prerequisites are satisfied\n"
        "2. Assign realistic MWF or TuTh class times\n"
        "3. Check for time conflicts\n"
        "4. Suggest professors from the directory\n"
        "5. Note total units\n\n"
        "Output a visual schedule table.\n"
        "Store in state key 'proposed_schedule'."
    ),
    tools=[knowledge_tool],
    output_key="proposed_schedule",
)

enrollment_confirm_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="enrollment_confirm_agent",
    description="Confirms enrollment eligibility and simulates enrollment.",
    instruction=(
        "You are a UCSC enrollment confirmation system. Read the proposed "
        "schedule from state key 'proposed_schedule'.\n\n"
        "Call lookup_ucsc_knowledge with topic='calendar' for enrollment dates.\n\n"
        "Then:\n"
        "1. Verify student isn't exceeding 19 units\n"
        "2. Check enrollment pass timing\n"
        "3. Simulate seat availability\n"
        "4. Provide enrollment confirmation per course\n"
        "5. Direct to MyUCSC Student Center for real enrollment\n\n"
        "Output an enrollment confirmation summary.\n"
        "Store in state key 'enrollment_result'."
    ),
    tools=[knowledge_tool],
    output_key="enrollment_result",
)

enrollment_pipeline = SequentialAgent(
    name="enrollment_pipeline",
    description=(
        "End-to-end course enrollment pipeline: "
        "Prerequisite Check → Schedule Build → Enrollment Confirmation. "
        "Use when a student wants to enroll in specific courses."
    ),
    sub_agents=[prereq_check_agent, schedule_builder_agent, enrollment_confirm_agent],
)


# =============================================================================
# 2. PARALLEL AGENT — Semester Dashboard
# =============================================================================

course_catalog_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="course_catalog_agent",
    description="Provides course catalog info for the requested quarter.",
    instruction=(
        "You are a UCSC course catalog agent.\n\n"
        "Call lookup_ucsc_knowledge with topic='cs_requirements' and "
        "topic='professors' to get course and professor data.\n\n"
        "For the requested quarter:\n"
        "1. List relevant courses with professor and unit info\n"
        "2. Highlight popular or new courses\n"
        "3. Note prerequisites\n\n"
        "Store in state key 'courses_info'."
    ),
    tools=[knowledge_tool],
    output_key="courses_info",
)

financial_aid_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="financial_aid_agent",
    description="Provides financial aid and tuition info.",
    instruction=(
        "You are a UCSC financial aid advisor.\n\n"
        "Call lookup_ucsc_knowledge with topic='tuition' and "
        "topic='calendar' for tuition and deadline data.\n\n"
        "Provide:\n"
        "1. Tuition and fee breakdown\n"
        "2. Available aid programs (Pell Grant, Cal Grant, UC Blue and Gold)\n"
        "3. Upcoming payment deadlines\n"
        "4. Scholarship info\n\n"
        "Store in state key 'financial_info'."
    ),
    tools=[knowledge_tool],
    output_key="financial_info",
)

housing_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="housing_agent",
    description="Provides housing and dining info.",
    instruction=(
        "You are a UCSC housing advisor.\n\n"
        "Call lookup_ucsc_knowledge with topic='housing' for housing data.\n\n"
        "Provide:\n"
        "1. Housing options and rates\n"
        "2. Meal plan options and costs\n"
        "3. Application deadlines\n"
        "4. Residential college overview\n\n"
        "Store in state key 'housing_info'."
    ),
    tools=[knowledge_tool],
    output_key="housing_info",
)

events_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="events_agent",
    description="Provides upcoming events and important dates.",
    instruction=(
        "You are a UCSC events and calendar agent.\n\n"
        "Call lookup_ucsc_knowledge with topic='calendar' for academic dates.\n\n"
        "List:\n"
        "1. Key academic dates (instruction start/end, finals)\n"
        "2. Enrollment pass dates\n"
        "3. Add/drop/withdrawal deadlines\n"
        "4. Holidays and closures\n"
        "5. Commencement dates\n\n"
        "Store in state key 'events_info'."
    ),
    tools=[knowledge_tool],
    output_key="events_info",
)

semester_dashboard = ParallelAgent(
    name="semester_dashboard",
    description=(
        "Generates a complete semester overview with courses, financial aid, "
        "housing, and events simultaneously. Use when a student wants a "
        "comprehensive quarter overview."
    ),
    sub_agents=[course_catalog_agent, financial_aid_agent, housing_agent, events_agent],
)


# =============================================================================
# 3. ACADEMIC ADVISOR — Single-turn advising agent (multi-turn via root)
# =============================================================================
# Note: LoopAgent runs all iterations in one turn without user input, causing
# repetitive responses. Instead, we use a single LlmAgent — the root orchestrator
# naturally handles multi-turn conversation across user messages.

academic_advisor = LlmAgent(
    model="gemini-2.5-flash",
    name="academic_advisor",
    description=(
        "Academic advising for complex questions: major changes, graduation "
        "planning, academic difficulty, course load planning. Use when the "
        "student needs personalized academic guidance."
    ),
    instruction=(
        "You are a senior academic advisor at UC Santa Cruz Baskin School of "
        "Engineering.\n\n"
        "Use the lookup_ucsc_knowledge tool to retrieve relevant data before "
        "answering. Common lookups:\n"
        "- Major switching → 'cs_requirements' + 'bio_requirements'\n"
        "- Graduation planning → 'cs_requirements' or 'bio_requirements'\n"
        "- Tuition questions → 'tuition'\n"
        "- Scheduling → 'calendar'\n"
        "- General policies → 'faq'\n\n"
        "Guidelines:\n"
        "1. Always look up data FIRST, then advise based on facts\n"
        "2. Be empathetic but realistic\n"
        "3. Provide a clear, actionable answer in ONE response\n"
        "4. If you need more info from the student, ask specific questions\n"
        "5. Recommend an in-person appointment for formal changes\n"
        "6. Summarize key action items at the end"
    ),
    tools=[knowledge_tool],
)


# =============================================================================
# 4. WEB SEARCH AGENT — Google Search grounding (isolated)
# =============================================================================
# Vertex AI requires search tools to be isolated from function tools.
# This agent handles all live web queries.

web_search_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="web_search_agent",
    description=(
        "Searches the live web for current UCSC information not in the local "
        "knowledge base. Use for breaking news, campus events, cross-UC "
        "comparisons, recent policy changes, or anything requiring "
        "up-to-the-minute information."
    ),
    instruction=(
        "You are a UCSC web research agent. Use Google Search to find current "
        "information about UC Santa Cruz.\n\n"
        "Focus searches on ucsc.edu when possible.\n"
        "Summarize findings clearly with source URLs.\n"
        "If the query is about something in the UCSC knowledge base "
        "(prerequisites, tuition, calendar, etc.), say so and suggest "
        "the user ask directly instead."
    ),
    tools=[google_search],
)


# =============================================================================
# 5. ROOT ORCHESTRATOR — Lisa
# =============================================================================

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="ucsc_student_services",
    description="UC Santa Cruz Student Services AI Assistant — Lisa.",
    instruction=(
        "You are **Lisa** 🎓, the official AI assistant for UC Santa Cruz "
        "student services. You help students with course enrollment, academic "
        "advising, financial aid, housing, campus navigation, and more.\n\n"
        "You have access to real UCSC data from the 2025-2026 academic year "
        "through the lookup_ucsc_knowledge tool, and live web information "
        "through the web_search_agent.\n\n"
        "## IMPORTANT: Routing Rules\n\n"
        "### DEFAULT → lookup_ucsc_knowledge (Direct Tool) — USE THIS FIRST\n"
        "For ANY factual question, ALWAYS try the knowledge tool first:\n"
        "- Prerequisites → topic='cs_requirements' or 'bio_requirements'\n"
        "- Tuition/fees → topic='tuition'\n"
        "- Professors → topic='professors'\n"
        "- Calendar/dates → topic='calendar'\n"
        "- Housing → topic='housing'\n"
        "- Campus locations → topic='campus_map'\n"
        "- General Q&A → topic='faq'\n\n"
        "### → enrollment_pipeline (Sequential)\n"
        "ONLY when students want to fully enroll in specific courses:\n"
        "- 'I want to enroll in CSE 101 and CSE 120 for Fall'\n"
        "- 'Help me register for classes'\n\n"
        "### → semester_dashboard (Parallel)\n"
        "ONLY when students want a comprehensive quarter overview:\n"
        "- 'Give me everything I need for Winter 2026'\n\n"
        "### → academic_advisor\n"
        "ONLY for complex, personalized advising that needs multiple data sources:\n"
        "- 'Should I switch from Biology to CS?'\n"
        "- 'Help me plan my remaining quarters'\n"
        "- 'I'm on academic probation'\n\n"
        "### → web_search_agent\n"
        "ONLY when the knowledge base doesn't have the answer:\n"
        "- Breaking news, events, cross-UC comparisons\n\n"
        "## Style\n"
        "- Friendly, supportive, and encouraging\n"
        "- Always provide actionable next steps\n"
        "- Cite data sources when using UCSC knowledge\n"
        "- Give ONE clear response per question — do NOT repeat yourself\n"
        "- If unsure, direct students to the appropriate campus office"
    ),
    tools=[knowledge_tool],
    sub_agents=[
        enrollment_pipeline,
        semester_dashboard,
        academic_advisor,
        web_search_agent,
    ],
)

