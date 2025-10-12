from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
import database
from models import TicketCreate, TicketUpdate, TicketResponse, TicketSummary

router = APIRouter()

# Response models
class MessageResponse(BaseModel):
    message: str

# Create ticket
@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    """
    Create a new ticket
    """
    try:
        # Convert Pydantic model to dict
        ticket_data = ticket.dict()
        
        # Generate ticket number if not provided
        if 'ticket_number' not in ticket_data:
            import datetime
            import random
            timestamp = datetime.datetime.now().strftime("%y%m%d")
            random_num = str(random.randint(1000, 9999))
            ticket_data['ticket_number'] = f"TKT-{timestamp}-{random_num}"
        
        # Create ticket in database
        created_ticket = await database.db.create_ticket(ticket_data)
        
        if not created_ticket:
            raise HTTPException(status_code=500, detail="Failed to create ticket")
        
        return created_ticket
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")

# Get all tickets with optional filtering and pagination
@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    category: Optional[str] = Query(None, description="Filter by category"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned person"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
):
    """
    Get all tickets with optional filtering and pagination
    """
    try:
        # Build filters
        filters = {}
        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if category:
            filters['category'] = category
        if assigned_to:
            filters['assigned_to'] = assigned_to
        
        tickets = await database.db.get_tickets(filters=filters, page=page, page_size=page_size)
        return tickets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tickets: {str(e)}")

# Get ticket by ID
@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str):
    """
    Get a specific ticket by ID
    """
    try:
        ticket = await database.db.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ticket: {str(e)}")

# Get ticket by ticket number
@router.get("/number/{ticket_number}", response_model=TicketResponse)
async def get_ticket_by_number(ticket_number: str):
    """
    Get a specific ticket by ticket number
    """
    try:
        ticket = await database.db.get_ticket_by_number(ticket_number)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ticket: {str(e)}")

# Update ticket
@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket_update: TicketUpdate):
    """
    Update a specific ticket
    """
    try:
        # Check if ticket exists
        existing_ticket = await database.db.get_ticket(ticket_id)
        if not existing_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Convert update data to dict, excluding unset fields
        update_data = ticket_update.dict(exclude_unset=True)
        
        # Update the ticket
        updated_ticket = await database.db.update_ticket(ticket_id, update_data)
        if not updated_ticket:
            raise HTTPException(status_code=500, detail="Failed to update ticket")
        
        return updated_ticket
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")

# Delete ticket
@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: str):
    """
    Delete a specific ticket
    """
    try:
        # Check if ticket exists
        existing_ticket = await database.db.get_ticket(ticket_id)
        if not existing_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Delete the ticket (you'll need to implement this method in database.py)
        success = await database.db.delete_ticket(ticket_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete ticket")
        
        return MessageResponse(message="Ticket deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting ticket: {str(e)}")

# Get ticket statistics
@router.get("/stats/summary", response_model=TicketSummary)
async def get_ticket_statistics():
    """
    Get ticket statistics summary
    """
    try:
        stats = await database.db.get_ticket_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

# Search tickets by keyword
@router.get("/search/{keyword}", response_model=List[TicketResponse])
async def search_tickets(
    keyword: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
):
    """
    Search tickets by keyword in title or description
    """
    try:
        # You'll need to implement this method in database.py
        tickets = await database.db.search_tickets(keyword, page=page, page_size=page_size)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tickets: {str(e)}")
