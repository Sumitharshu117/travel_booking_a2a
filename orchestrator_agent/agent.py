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

# Activities Agent
activities_agent = RemoteA2aAgent(
    name="activities_agent",
    description=(
        "Searches sightseeing tours, tourist attractions "
        "and activities."
    ),
    agent_card=(
        "http://localhost:8004"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)

# Payment Agent
payment_agent = RemoteA2aAgent(
    name="payment_agent",
    description=(
        "Validates payment requests and processes "
        "mock payments after user approval."
    ),
    agent_card=(
        "http://localhost:8005"
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
        You are a Travel Booking Orchestrator.
        plan accroding to the user's travel request by coordinating with specialist agents.
        do it in plans 
        You coordinate the following specialist agents:
        - flight_agent
        - hotel_agent
        - transport_agent
        - activities_agent
        - payment_agent

        For every complete travel-planning request:

        1. Identify which services the user requested.
        2. Delegate flight searches to flight_agent.
        3. Delegate hotel searches to hotel_agent.
        4. Delegate airport transfer searches to transport_agent.
        5. Delegate activity searches to activities_agent.
        6. Collect the results from all requested agents.
        7. Combine the results into one organized travel plan.
        8. Calculate an estimated total from the actual returned prices.

        Do not stop after receiving the result from one agent.
        Do not invent results if an agent fails.
        Clearly report any agent that could not provide a result.

        IMPORTANT:
        - Payment must only happen after showing the user the total
        and receiving explicit approval.
        - Never claim that a real booking or payment was completed.
    """,
    sub_agents=[
        flight_agent,
        hotel_agent,
        transport_agent,
        activities_agent,
        payment_agent
    ]
)