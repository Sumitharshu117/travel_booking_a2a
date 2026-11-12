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


def search_activities(
    city: str,
    participants: int,
    category: str = "any",
    visit_date: str = "not specified"
) -> dict:
    """Search tourist activities in a city.

    Args:
        city: Destination city.
        participants: Number of people.
        category: Activity category or any.
        visit_date: Visit date in YYYY-MM-DD format.
    """

    activities = [
        {
            "activity_id": "ACT101",
            "name": "Eiffel Tower Visit",
            "city": "Paris",
            "category": "landmark",
            "price_per_person": 2500,
            "currency": "INR",
            "duration": "2 hours"
        },
        {
            "activity_id": "ACT102",
            "name": "Louvre Museum",
            "city": "Paris",
            "category": "museum",
            "price_per_person": 1800,
            "currency": "INR",
            "duration": "3 hours"
        },
        {
            "activity_id": "ACT103",
            "name": "Seine River Cruise",
            "city": "Paris",
            "category": "cruise",
            "price_per_person": 2200,
            "currency": "INR",
            "duration": "1 hour"
        },
        {
            "activity_id": "ACT104",
            "name": "Paris City Sightseeing",
            "city": "Paris",
            "category": "guided tour",
            "price_per_person": 3000,
            "currency": "INR",
            "duration": "4 hours"
        },
        {
            "activity_id": "ACT105",
            "name": "Versailles Palace Tour",
            "city": "Paris",
            "category": "day trip",
            "price_per_person": 4500,
            "currency": "INR",
            "duration": "6 hours"
        }
    ]

    matching_activities = [
        activity for activity in activities
        if activity["city"].lower() == city.lower()
        and (
            category.lower() == "any"
            or activity["category"].lower() == category.lower()
        )
    ]

    if not matching_activities:
        return {
            "status": "no_results",
            "message": f"No sample activities found for {city}.",
            "activities": []
        }

    results = []

    for activity in matching_activities:
        result = activity.copy()
        result["participants"] = participants
        result["total_estimated_price"] = (
            activity["price_per_person"] * participants
        )
        results.append(result)

    return {
        "status": "success",
        "city": city,
        "visit_date": visit_date,
        "participants": participants,
        "activities": results
    }


root_agent = Agent(
    name="activities_agent",
    model="gemini-3.6-flash",
    description=(
        "A travel activities specialist that searches "
        "sightseeing tours, attractions and experiences."
    ),
    instruction="""
    You are a professional Activities and Tours Agent.

    Your responsibilities:

    1. Understand the traveler's activity requirements.
    2. Identify the destination city.
    3. Identify the number of participants.
    4. Identify the preferred activity category.
    5. Identify the visit date.
    6. Use search_activities to find matching activities.
    7. Compare prices and durations.
    8. Present the results clearly.

    Rules:
    - Only report activities returned by the tool.
    - Never invent prices or availability.
    - Clearly distinguish estimated prices from confirmed tickets.
    - These are mock activity records.
    - Do not claim that tickets have been purchased.
    - Ask for missing essential information.
    """,
    tools=[search_activities]
)