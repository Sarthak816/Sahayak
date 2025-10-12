from typing import List
import asyncio
import aiohttp
import random
from datetime import datetime, timedelta

# Base URL for your API
BASE_URL = "http://localhost:8000/api/v1/ticket"

# Sample data for generating realistic tickets
SAMPLE_CATEGORIES = ["Technical", "Billing", "Feature Request", "Bug Report", "Account", "General Inquiry"]
SAMPLE_PRIORITIES = ["Low", "Medium", "High", "Urgent"]
SAMPLE_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
SAMPLE_ASSIGNEES = ["alice@company.com", "bob@company.com", "charlie@company.com", "diana@company.com", None]

SAMPLE_TITLES = [
    "Login issues with the new update",
    "Payment processing failed",
    "Feature suggestion: dark mode",
    "Database connection timeout",
    "Mobile app crashing on startup",
    "Password reset not working",
    "Invoice download problem",
    "UI alignment issues on dashboard"
]

SAMPLE_DESCRIPTIONS = [
    "I'm unable to login with my credentials after the latest update. Getting authentication error.",
    "When trying to process payment, the system returns an internal server error.",
    "It would be great to have a dark mode option for better nighttime usage.",
    "The application frequently times out when connecting to the database during peak hours.",
    "The mobile app crashes immediately after splash screen on iOS 16.5.",
    "Password reset emails are not being received by users.",
    "Downloaded invoices are corrupted and cannot be opened.",
    "The dashboard elements are misaligned on 4K monitor resolutions."
]

async def create_sample_ticket(session: aiohttp.ClientSession, ticket_data: dict) -> dict:
    """
    Create a single ticket via the API
    """
    try:
        async with session.post(f"{BASE_URL}/", json=ticket_data) as response:
            if response.status == 200:
                result = await response.json()
                print(f"✓ Created ticket: {result.get('ticket_number', 'Unknown')}")
                return result
            else:
                error_text = await response.text()
                print(f"✗ Failed to create ticket: {response.status} - {error_text}")
                return None
    except Exception as e:
        print(f"✗ Error creating ticket: {str(e)}")
        return None

def generate_sample_ticket(index: int) -> dict:
    """
    Generate a realistic sample ticket with random data
    """
    # Generate random dates within the last 30 days
    created_date = datetime.now() - timedelta(days=random.randint(0, 30))
    updated_date = created_date + timedelta(hours=random.randint(1, 72))
    
    # 80% chance of having an assignee
    has_assignee = random.random() > 0.2
    
    ticket_data = {
        "title": f"{random.choice(SAMPLE_TITLES)} #{index}",
        "description": random.choice(SAMPLE_DESCRIPTIONS),
        "category": random.choice(SAMPLE_CATEGORIES),
        "priority": random.choice(SAMPLE_PRIORITIES),
        "status": random.choice(SAMPLE_STATUSES),
        "assigned_to": random.choice(SAMPLE_ASSIGNEES) if has_assignee else None,
        "reporter_email": f"user{index}@example.com",
        "created_date": created_date.isoformat(),
        "updated_date": updated_date.isoformat()
    }
    
    # Add optional fields with some probability
    if random.random() > 0.7:  # 30% chance
        ticket_data["due_date"] = (datetime.now() + timedelta(days=random.randint(1, 14))).isoformat()
    
    if random.random() > 0.5:  # 50% chance
        ticket_data["tags"] = ["customer-reported", "v2.1"]
    
    return ticket_data

async def create_sample_tickets(num_tickets: int = 20):
    """
    Create multiple sample tickets asynchronously
    """
    print(f"Creating {num_tickets} sample tickets...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_tickets):
            ticket_data = generate_sample_ticket(i + 1)
            task = create_sample_ticket(session, ticket_data)
            tasks.append(task)
        
        # Limit concurrent requests to avoid overwhelming the server
        batch_size = 5
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)
            
            # Small delay between batches
            if i + batch_size < len(tasks):
                await asyncio.sleep(0.1)
        
        successful = [r for r in results if r is not None and not isinstance(r, Exception)]
        print("=" * 50)
        print(f"Successfully created {len(successful)} out of {num_tickets} tickets")
        
        return successful

async def verify_tickets_created(session: aiohttp.ClientSession):
    """
    Verify that tickets were created by fetching the ticket list
    """
    try:
        async with session.get(f"{BASE_URL}/") as response:
            if response.status == 200:
                tickets = await response.json()
                print(f"\nVerification: Found {len(tickets)} tickets in the system")
                if tickets:
                    print("Sample of created tickets:")
                    for ticket in tickets[:3]:  # Show first 3 tickets
                        print(f"  - {ticket.get('ticket_number')}: {ticket.get('title')}")
                return tickets
            else:
                print(f"Verification failed: {response.status}")
                return []
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return []

async def main():
    """
    Main function to run the sample data creation
    """
    print("FastAPI Ticket System - Sample Data Generator")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print()
    
    try:
        # Create sample tickets
        created_tickets = await create_sample_tickets(15)
        
        # Verify creation
        async with aiohttp.ClientSession() as session:
            await verify_tickets_created(session)
            
    except aiohttp.ClientConnectorError:
        print("\n❌ Error: Cannot connect to the FastAPI server.")
        print("Please make sure your server is running on http://localhost:8000")
        print("Start it with: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

def create_simple_sample():
    """
    Synchronous version for simple testing without async
    """
    import requests
    
    sample_ticket = {
        "title": "Sample Ticket - Login Issue",
        "description": "Users are unable to login with correct credentials after the recent update.",
        "category": "Technical",
        "priority": "High",
        "status": "Open",
        "reporter_email": "testuser@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/", json=sample_ticket)
        if response.status_code == 200:
            print(f"✓ Created sample ticket: {response.json().get('ticket_number')}")
        else:
            print(f"✗ Failed to create ticket: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("Make sure the FastAPI server is running!")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
    
    # Uncomment the line below for a simple synchronous version
    # create_simple_sample()
