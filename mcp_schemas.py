"""
Minimal Pydantic schemas and mock data for MCP tools
Only includes models used by the 'yes' marked functions
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date, timedelta
from enum import Enum
import uuid

# Enums
class AgentType(str, Enum):
    recognition = "recognition"
    behaviour_matcher = "behaviour_matcher"
    points_calculator = "points_calculator"
    points_self_service = "points_self_service"
    recognition_summary = "recognition_summary"
    service_anniversary = "service_anniversary"
    send_recognition = "send_recognition"

class StatusType(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"

# Base Models
class ContextBase(BaseModel):
    agent_type: AgentType
    purpose: Optional[str] = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    validation_errors: Optional[List[str]] = None

class BaseResponse(BaseModel):
    status: StatusType
    error: Optional[ErrorDetail] = None

# Request Models (only for 'yes' functions)
class GetRecognitionsRequest(BaseModel):
    user_id: str
    tenant_id: str
    context: Dict[str, Any]
    target_user_id: Optional[str] = None

class SendRecognitionRequest(BaseModel):
    sender_id: str
    recipient_id: str
    tenant_id: str
    recognition_details: Dict[str, Any]
    context: Dict[str, Any]
    validation_override: Optional[bool] = False

class LookupTeamRequest(BaseModel):
    user_id: str
    tenant_id: str
    context: Dict[str, Any]
    filters: Optional[Dict[str, Any]] = {}

class GroupRecognitionRequest(BaseModel):
    user_id: str
    tenant_id: str
    context: Dict[str, Any]
    filters: Optional[Dict[str, Any]] = {}

class PostRecognitionRequest(BaseModel):
    sender_id: str
    celebrant_id: str
    tenant_id: str
    anniversary_details: Dict[str, Any]
    context: Dict[str, Any]
    additional_data: Optional[Dict[str, Any]] = {}

class CelebrationInviteRequest(BaseModel):
    sender_id: str
    celebrant_id: str
    tenant_id: str
    celebration_details: Dict[str, Any]
    invite_criteria: Dict[str, Any]
    context: Dict[str, Any]

# Response Models (only for 'yes' functions)
class RecognitionsResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class SendRecognitionResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    warnings: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

class TeamResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class GroupRecognitionResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class PostRecognitionResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class CelebrationInviteResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

# Mock Data Storage
class MockDataStore:
    def __init__(self):
        self.users = {
            "user1": {
                "user_id": "user1",
                "basic_info": {
                    "name": "Sarah Johnson",
                    "email": "sarah.johnson@company.com",
                    "display_name": "Sarah J.",
                    "avatar_url": "https://example.com/avatars/sarah.jpg"
                },
                "role_info": {
                    "title": "Senior Software Engineer",
                    "department": "Engineering",
                    "team": "Platform Team",
                    "manager_id": "mgr1",
                    "direct_reports": ["user3", "user4"],
                    "role_level": "Senior"
                },
                "employment_info": {
                    "employee_id": "EMP001",
                    "hire_date": "2019-03-15",
                    "tenure_years": 5.5,
                    "location": "San Francisco",
                    "timezone": "America/Los_Angeles"
                }
            },
            "user2": {
                "user_id": "user2",
                "basic_info": {
                    "name": "Mike Chen",
                    "email": "mike.chen@company.com",
                    "display_name": "Mike C.",
                    "avatar_url": "https://example.com/avatars/mike.jpg"
                },
                "role_info": {
                    "title": "Product Manager",
                    "department": "Product",
                    "team": "Growth Team",
                    "manager_id": "mgr2",
                    "direct_reports": ["user5"],
                    "role_level": "Mid"
                },
                "employment_info": {
                    "employee_id": "EMP002",
                    "hire_date": "2020-01-10",
                    "tenure_years": 4.8,
                    "location": "Remote",
                    "timezone": "America/New_York"
                }
            }
        }
        
        self.programs = {
            "prog1": {
                "program_id": "prog1",
                "name": "Peer Recognition Program",
                "description": "Recognize colleagues for exceptional work and collaboration",
                "type": "recognition",
                "status": "active",
                "validity": {
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": "2024-12-31T23:59:59Z"
                },
                "budget_config": {
                    "total_budget": 100000,
                    "individual_limit": 500,
                    "frequency_limit": "monthly",
                    "currency": "USD"
                },
                "point_values": {
                    "min_points": 10,
                    "max_points": 100,
                    "default_points": 25,
                    "point_increments": 5
                },
                "behaviors": [
                    {
                        "behavior_id": "collab1",
                        "name": "Exceptional Collaboration",
                        "description": "Goes above and beyond to help teammates succeed",
                        "criteria": "Demonstrates outstanding teamwork and cross-functional collaboration",
                        "suggested_points": 50
                    },
                    {
                        "behavior_id": "innov1", 
                        "name": "Innovation Excellence",
                        "description": "Brings creative solutions to complex problems",
                        "criteria": "Shows innovative thinking that drives business results",
                        "suggested_points": 75
                    }
                ]
            },
            "prog2": {
                "program_id": "prog2",
                "name": "Service Anniversary Program",
                "description": "Celebrate employee milestones and tenure",
                "type": "anniversary",
                "status": "active",
                "validity": {
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": "2024-12-31T23:59:59Z"
                },
                "budget_config": {
                    "total_budget": 50000,
                    "individual_limit": 1000,
                    "frequency_limit": "yearly",
                    "currency": "USD"
                },
                "point_values": {
                    "min_points": 100,
                    "max_points": 500,
                    "default_points": 200,
                    "point_increments": 25
                }
            }
        }

        self.recognitions = []
        self.budgets = {
            "user1": {"allocated": 500, "spent": 150, "remaining": 350},
            "user2": {"allocated": 500, "spent": 200, "remaining": 300}
        }

# Global instance
mock_store = MockDataStore()
