
from google.adk.agents import Agent

import os
from pathlib import Path
from dotenv import load_dotenv

# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the root .env file
load_dotenv(PROJECT_ROOT / ".env")

# Verify that the API key exists
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError(
        "GOOGLE_API_KEY not found. Check your root .env file."
    )
# Tool 1: Search available flights
def search_flights(
    origin: str,
    destination: str,
    travel_date: str
) -> dict:
    """
    Search flights between two airports.

    Args:
        origin: Origin airport code.
        destination: Destination airport code.
        travel_date: Travel date in YYYY-MM-DD format.
    """

    # Mock flight data for learning
    flights = [
        {
            "flight_number": "AI101",
            "airline": "Air India",
            "departure": "10:00",
            "arrival": "18:30",
            "price": 42000,
            "currency": "INR"
        },
        {
            "flight_number": "EK567",
            "airline": "Emirates",
            "departure": "14:00",
            "arrival": "22:15",
            "price": 51000,
            "currency": "INR"
        }
    ]

    return {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "travel_date": travel_date,
        "flights": flights
    }


# Create the Gemini-powered ADK agent
root_agent = Agent(
    name="flight_agent",

    model="gemini-3.6-flash",

    description=(
        "An AI flight booking specialist "
        "that searches and compares flights."
    ),

    instruction="""
    You are a professional flight booking agent.

    Your responsibilities:
    1. Understand the user's flight requirements.
    2. Identify origin and destination.
    3. Identify the travel date.
    4. Use search_flights to search available flights.
    5. Compare the available flights.
    6. Present prices and timings clearly.

    Never invent flight availability.
    Only report results returned by your tools.

    Do not confirm or charge for a booking.
    """,

    tools=[search_flights]
)
