import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

# Load Gemini API key
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY not found.")


# Flight Agent
flight_agent = RemoteA2aAgent(
    name="flight_agent",
    description="Searches and compares flights.",
    agent_card=(
        "http://localhost:8001"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)


# Hotel Agent
hotel_agent = RemoteA2aAgent(
    name="hotel_agent",
    description="Searches and compares hotels.",
    agent_card=(
        "http://localhost:8002"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)


# Transport Agent
transport_agent = RemoteA2aAgent(
    name="transport_agent",
    description="Finds airport transfers and suitable vehicles.",
    agent_card=(
        "http://localhost:8003"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)


# Main Orchestrator
root_agent = Agent(
    name="travel_orchestrator",
    model="gemini-3.6-flash",
    description="Coordinates travel booking specialist agents.",

    instruction="""
    You are a professional Travel Orchestrator.

    You have three specialist agents:

    1. flight_agent:
       Searches and compares flights.

    2. hotel_agent:
       Searches and compares hotels.

    3. transport_agent:
       Finds airport transfer vehicles and estimates fares.

    Responsibilities:

    - Understand the user's travel requirements.
    - Delegate each request to the appropriate specialist.
    - Pass all required information to the specialist.
    - Wait for their responses.
    - Combine their results into a clear travel summary.
    - Never invent prices or availability.
    - Never claim that anything is booked.

    For flights, collect:
    - Origin
    - Destination
    - Travel date

    For hotels, collect:
    - City
    - Check-in
    - Check-out
    - Guests

    For transport, collect:
    - Airport
    - Destination
    - Passengers
    - Luggage count
    - Preferred vehicle, if specified

    Ask for missing essential information.
    """,
    sub_agents=[
        flight_agent,
        hotel_agent,
        transport_agent
    ]
)