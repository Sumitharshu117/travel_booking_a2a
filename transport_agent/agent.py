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

def search_transport(
    airport: str,
    destination: str,
    passengers: int,
    luggage: int,
    vehicle_type: str = "any"
) -> dict:
    """Find suitable airport transfer vehicles.

    Args:
        airport: Airport name or code.
        destination: Hotel, address, or destination area.
        passengers: Number of passengers.
        luggage: Number of luggage bags.
        vehicle_type: Preferred vehicle type or any.
    """

    vehicles = [
        {
            "vehicle_id": "CAB101",
            "vehicle_type": "Sedan",
            "capacity": 3,
            "luggage_capacity": 3,
            "price": 4500,
            "currency": "INR"
        },
        {
            "vehicle_id": "CAB102",
            "vehicle_type": "SUV",
            "capacity": 5,
            "luggage_capacity": 5,
            "price": 6500,
            "currency": "INR"
        },
        {
            "vehicle_id": "CAB103",
            "vehicle_type": "Van",
            "capacity": 8,
            "luggage_capacity": 8,
            "price": 9000,
            "currency": "INR"
        }
    ]

    matching_vehicles = []

    for vehicle in vehicles:
        enough_passengers = (
            vehicle["capacity"] >= passengers
        )

        enough_luggage = (
            vehicle["luggage_capacity"] >= luggage
        )

        preferred_type = (
            vehicle_type.lower() == "any"
            or vehicle["vehicle_type"].lower()
            == vehicle_type.lower()
        )

        if (
            enough_passengers
            and enough_luggage
            and preferred_type
        ):
            matching_vehicles.append(vehicle)

    if not matching_vehicles:
        return {
            "status": "no_results",
            "message": "No suitable vehicle found.",
            "vehicles": []
        }

    return {
        "status": "success",
        "airport": airport,
        "destination": destination,
        "passengers": passengers,
        "luggage": luggage,
        "vehicles": matching_vehicles
    }


root_agent = Agent(
    name="transport_agent",
    model="gemini-3.6-flash",
    description=(
        "An airport transportation specialist "
        "that finds suitable vehicles and estimates fares."
    ),
    instruction="""
    You are a professional Airport Transport Agent.

    Your responsibilities:

    1. Understand airport transfer requirements.
    2. Identify the airport.
    3. Identify the destination.
    4. Identify passenger count.
    5. Identify luggage count.
    6. Identify preferred vehicle type.
    7. Call search_transport.
    8. Compare suitable vehicles.
    9. Present the fare estimates.

    Rules:
    - Never invent vehicle options or prices.
    - Use only the search tool results.
    - Do not claim a vehicle has been booked.
    - These are mock transport prices.
    - Ask for missing essential details.
    """,
    tools=[search_transport]
)