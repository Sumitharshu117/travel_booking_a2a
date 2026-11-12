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



import uuid
from google.adk.agents import Agent

transactions = {}


def process_mock_payment(
    amount: float,
    currency: str,
    idempotency_key: str,
    approved: bool
) -> dict:
    """Simulate a payment after explicit user approval.

    Args:
        amount: Total amount to be paid.
        currency: Payment currency, currently INR only.
        idempotency_key: Unique key for this payment attempt.
        approved: True only after the user explicitly approves.
    """

    if not approved:
        return {
            "status": "approval_required",
            "message": "Payment requires explicit user approval."
        }

    if amount <= 0:
        return {
            "status": "failed",
            "message": "Payment amount must be greater than zero."
        }

    if currency.upper() != "INR":
        return {
            "status": "failed",
            "message": "This mock payment agent supports INR only."
        }

    if not idempotency_key.strip():
        return {
            "status": "failed",
            "message": "An idempotency key is required."
        }

    # Prevent duplicate processing for the same key.
    if idempotency_key in transactions:
        return {
            **transactions[idempotency_key],
            "message": "Previously processed payment returned."
        }

    transaction = {
        "status": "success",
        "transaction_id": f"MOCK-{uuid.uuid4().hex[:12].upper()}",
        "amount": amount,
        "currency": "INR",
        "payment_mode": "MOCK",
        "message": "Mock payment processed successfully."
    }

    transactions[idempotency_key] = transaction

    return transaction


root_agent = Agent(
    name="payment_agent",
    model="gemini-3.6-flash",
    description=(
        "A mock payment specialist that validates payment requests "
        "and simulates payment processing."
    ),
    instruction="""
    You are a Payment Processing Agent.

    Your responsibilities:
    1. Receive a payment request from the orchestrator.
    2. Check the requested amount and currency.
    3. Require explicit user approval before processing.
    4. Use process_mock_payment to simulate payment.
    5. Return the transaction ID and payment status.

    Strict rules:
    - Never process a payment without explicit user approval.
    - Never invent a transaction ID.
    - Never claim a real payment was made.
    - This is a mock payment system.
    - Never request or store card numbers, CVVs,
      passwords or banking credentials.
    - Never change the amount provided by the orchestrator.
    - Return the actual result from the payment tool.
    """,
    tools=[process_mock_payment]
)