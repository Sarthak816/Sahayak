from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    PENDING_CUSTOMER = "pending_customer"
    PENDING_VENDOR = "pending_vendor"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketSource(str, Enum):
    CHATBOT = "chatbot"
    EMAIL = "email"
    GLPI = "glpi"
    SOLMAN = "solman"
    MANUAL = "manual"
    PHONE = "phone"

class TicketCategory(str, Enum):
    PASSWORD_RESET = "password_reset"
    VPN_ACCESS = "vpn_access"
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    EMAIL_ISSUES = "email_issues"
    ACCESS_RIGHTS = "access_rights"
    OTHER = "other"

class TicketBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, description="Brief description of the issue")
    description: str = Field(..., min_length=10, description="Detailed description of the problem")
    category: TicketCategory
    priority: TicketPriority = TicketPriority.MEDIUM
    source: TicketSource
    assigned_team: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class TicketCreate(TicketBase):
    requester_email: EmailStr
    requester_name: str
    department: Optional[str] = None
    contact_number: Optional[str] = None
    related_assets: Optional[List[str]] = None

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_team: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None
    tags: Optional[List[str]] = None

class TicketInDB(TicketBase):
    id: str
    ticket_number: str
    status: TicketStatus = TicketStatus.OPEN
    requester_email: EmailStr
    requester_name: str
    department: Optional[str] = None
    contact_number: Optional[str] = None
    related_assets: Optional[List[str]] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    sla_due_date: Optional[datetime] = None
    ai_classification_confidence: Optional[float] = None
    suggested_knowledge_base_articles: List[str] = Field(default_factory=list)
    is_self_service_resolved: bool = False
    chat_history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class TicketResponse(TicketInDB):
    pass

class TicketSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    high_priority_tickets: int
    critical_tickets: int

class NotificationConfig(BaseModel):
    email_alerts: bool = True
    sms_alerts: bool = False
    notify_on_status_change: bool = True
    notify_on_assignment: bool = True
    notify_on_sla_breach: bool = True
    notify_on_resolution: bool = True
