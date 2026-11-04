from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)


# Remote Flight Agent
flight_agent = RemoteA2aAgent(
    name="flight_agent",
    description="Searches and compares flight options.",
    agent_card=(
        "http://localhost:8001"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)


# Remote Hotel Agent
hotel_agent = RemoteA2aAgent(
    name="hotel_agent",
    description="Searches and compares hotel options.",
    agent_card=(
        "http://localhost:8002"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)


# Main Travel Orchestrator
root_agent = Agent(
    name="travel_orchestrator",
    model="gemini-flash-latest",
    description="Coordinates flight and hotel search agents.",
    instruction="""
    You are a professional Travel Orchestrator.

    You have two specialist agents:

    1. flight_agent:
       Searches and compares flights.

    2. hotel_agent:
       Searches and compares hotels.

    Your responsibilities:

    - Understand the user's travel requirements.
    - Delegate flight requests to flight_agent.
    - Delegate hotel requests to hotel_agent.
    - Pass all relevant information to the correct agent.
    - Wait for the specialist agent's response.
    - Summarize the returned results.
    - Never invent availability or prices.
    - Never claim a booking has been confirmed.

    For hotel searches, collect:
    - Destination city
    - Check-in date
    - Check-out date
    - Number of guests

    For flight searches, collect:
    - Origin
    - Destination
    - Travel date

    If required information is missing, ask the user.
    """,
    sub_agents=[
        flight_agent,
        hotel_agent
    ]
)