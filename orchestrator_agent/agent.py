from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

# Connect to the remote Flight Agent using its Agent Card
flight_agent = RemoteA2aAgent(
    name="flight_agent",
    description=(
        "A remote specialist agent that searches and compares "
        "flights between airports."
    ),
    agent_card=(
        "http://127.0.0.1:8001"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
    use_legacy=False,
)

# Main Travel Orchestrator
root_agent = Agent(
    name="travel_orchestrator",
    model="gemini-3.6-flash",
    description=(
        "A travel planning orchestrator that delegates flight "
        "search requests to a remote Flight Agent."
    ),
    instruction="""
    You are a professional Travel Orchestrator.

    You coordinate independent specialist agents.

    Your available specialist:
    - flight_agent: Searches and compares flights.

    Rules:
    1. Understand the user's travel request.
    2. If the user asks to search for flights,
       delegate the task to flight_agent.
    3. Pass the origin, destination, and travel date
       clearly to flight_agent.
    4. Wait for the remote agent's response.
    5. Summarize the returned flight options.
    6. Never invent flight availability or prices.
    7. Do not claim a flight is booked.
    8. If required travel details are missing,
       ask the user for clarification.
    """,
    sub_agents=[flight_agent],
)