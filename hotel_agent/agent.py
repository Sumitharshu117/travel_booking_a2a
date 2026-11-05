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

def search_hotels(
    city: str,
    check_in: str,
    check_out: str,
    guests: int
) -> dict:
    """Search hotels in a city for the requested dates.

    Args:
        city: Destination city, for example Paris.
        check_in: Check-in date in YYYY-MM-DD format.
        check_out: Check-out date in YYYY-MM-DD format.
        guests: Number of guests.
    """

    hotels = [
        {
            "hotel_id": "PAR101",
            "name": "Hotel Eiffel Comfort",
            "city": "Paris",
            "star_rating": 3,
            "price_per_night": 8500,
            "currency": "INR",
            "amenities": ["WiFi", "Breakfast", "Air conditioning"]
        },
        {
            "hotel_id": "PAR102",
            "name": "Paris Grand Suites",
            "city": "Paris",
            "star_rating": 4,
            "price_per_night": 12500,
            "currency": "INR",
            "amenities": ["WiFi", "Breakfast", "Pool", "Gym"]
        },
        {
            "hotel_id": "PAR103",
            "name": "Luxury Champs Hotel",
            "city": "Paris",
            "star_rating": 5,
            "price_per_night": 22000,
            "currency": "INR",
            "amenities": ["WiFi", "Breakfast", "Pool", "Spa"]
        }
    ]

    matching_hotels = [
        hotel for hotel in hotels
        if hotel["city"].lower() == city.lower()
    ]

    if not matching_hotels:
        return {
            "status": "no_results",
            "message": f"No mock hotel inventory found for {city}.",
            "hotels": []
        }

    return {
        "status": "success",
        "city": city,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "hotels": matching_hotels
    }


root_agent = Agent(
    name="hotel_agent",
    model="gemini-3.6-flash",
    description=(
        "A hotel specialist that searches and compares "
        "hotel options for travelers."
    ),
    instruction="""
    You are a professional Hotel Booking Agent.

    Your responsibilities:
    1. Understand the user's hotel requirements.
    2. Identify the destination city.
    3. Identify check-in and check-out dates.
    4. Identify the number of guests.
    5. Use search_hotels to retrieve hotel options.
    6. Compare prices and star ratings.
    7. Present the results clearly.

    Important rules:
    - Only report hotels returned by the search tool.
    - Never invent availability or prices.
    - These are sample inventory records, not live bookings.
    - Do not confirm or charge for a reservation.
    - If required details are missing, ask the user.
    """,
    tools=[search_hotels]
)