from supabase import create_client
import os
from typing import Optional

class Database:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        self.client = create_client(supabase_url, supabase_key)
    
    async def create_ticket(self, ticket_data: dict) -> dict:
        """Create a new ticket in the database"""
        try:
            result = self.client.table('tickets').insert(ticket_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return None
    
    async def get_ticket(self, ticket_id: str) -> Optional[dict]:
        """Retrieve a ticket by ID"""
        try:
            result = self.client.table('tickets').select('*').eq('id', ticket_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching ticket: {e}")
            return None
    
    async def get_ticket_by_number(self, ticket_number: str) -> Optional[dict]:
        """Retrieve a ticket by ticket number"""
        try:
            result = self.client.table('tickets').select('*').eq('ticket_number', ticket_number).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching ticket: {e}")
            return None
    
    async def update_ticket(self, ticket_id: str, update_data: dict) -> Optional[dict]:
        """Update a ticket"""
        try:
            update_data['updated_at'] = 'now()'
            result = self.client.table('tickets').update(update_data).eq('id', ticket_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating ticket: {e}")
            return None
    
    async def get_tickets(self, filters: dict = None, page: int = 1, page_size: int = 50) -> list:
        """Retrieve tickets with optional filtering and pagination"""
        try:
            query = self.client.table('tickets').select('*')
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query = query.eq(key, value)
            
            # Apply pagination
            start = (page - 1) * page_size
            end = start + page_size - 1
            query = query.range(start, end)
            
            # Order by creation date (newest first)
            query = query.order('created_at', desc=True)
            
            result = query.execute()
            return result.data
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            return []
    
    async def get_ticket_statistics(self) -> dict:
        """Get ticket statistics for dashboard"""
        try:
            # This would typically be a database view or stored procedure
            # For now, we'll simulate with multiple queries
            total = self.client.table('tickets').select('*', count='exact').execute()
            open_tickets = self.client.table('tickets').select('*', count='exact').eq('status', 'open').execute()
            in_progress = self.client.table('tickets').select('*', count='exact').eq('status', 'in_progress').execute()
            high_priority = self.client.table('tickets').select('*', count='exact').eq('priority', 'high').execute()
            critical = self.client.table('tickets').select('*', count='exact').eq('priority', 'critical').execute()
            
            return {
                'total_tickets': total.count or 0,
                'open_tickets': open_tickets.count or 0,
                'in_progress_tickets': in_progress.count or 0,
                'high_priority_tickets': high_priority.count or 0,
                'critical_tickets': critical.count or 0
            }
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {}

    async def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket by ID"""
        try:
            result = self.client.table('tickets').delete().eq('id', ticket_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting ticket: {e}")
            return False

    async def search_tickets(self, keyword: str, page: int = 1, page_size: int = 50) -> list:
        """Search tickets by keyword in title or description"""
        try:
            start = (page - 1) * page_size
            end = start + page_size - 1
            
            result = self.client.table('tickets')\
                .select('*')\
                .or_(f"title.ilike.%{keyword}%,description.ilike.%{keyword}%")\
                .range(start, end)\
                .order('created_at', desc=True)\
                .execute()
            
            return result.data
        except Exception as e:
            print(f"Error searching tickets: {e}")
            return []
