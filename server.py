import os
import re
import uuid
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from mcp_schemas import (
    mock_store, 
    StatusType, 
    ErrorDetail,
    BaseResponse,
    RecognitionsResponse,
    TeamResponse,
    GroupRecognitionResponse,
    PostRecognitionResponse,
    CelebrationInviteResponse
)

mcp = FastMCP("Service_Anniversary MCP Server")


@mcp.tool(description="Show recognition history and points received/sent. Args: user_id (str), tenant_id (str), context (Dict[str, Any]), target_user_id (Optional[str]). Returns: Dict[str, Any] - RecognitionsResponse with status, data (summary, recognitions, analytics) and metadata.")
def get_recognitions(user_id: str,
    tenant_id: str,
    context: Dict[str, Any],
    target_user_id: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        target_id = target_user_id or user_id

        # Generate mock recognition data
        recognitions = [
            {
                "recognition_id": str(uuid.uuid4()),
                "type": "sent",
                "sender_id": target_id,
                "sender_name": mock_store.users[target_id]["basic_info"]["name"] if target_id in mock_store.users else "Unknown",
                "recipient_id": "user2",
                "recipient_name": "Mike Chen",
                "program_id": "prog1",
                "program_name": "Peer Recognition Program",
                "behavior_id": "collab1",
                "behavior_name": "Exceptional Collaboration",
                "points": 50,
                "title": "Great teamwork!",
                "message": "Thanks for helping with the project deadline",
                "date": (datetime.now() - timedelta(days=2)).isoformat(),
                "status": "completed",
                "visibility": "public"
            },
            {
                "recognition_id": str(uuid.uuid4()),
                "type": "received",
                "sender_id": "user2", 
                "sender_name": "Mike Chen",
                "recipient_id": target_id,
                "recipient_name": mock_store.users[target_id]["basic_info"]["name"] if target_id in mock_store.users else "Unknown",
                "program_id": "prog1",
                "program_name": "Peer Recognition Program",
                "behavior_id": "innov1",
                "behavior_name": "Innovation Excellence",
                "points": 75,
                "title": "Innovative solution!",
                "message": "Your creative approach saved the day",
                "date": (datetime.now() - timedelta(days=5)).isoformat(),
                "status": "completed",
                "visibility": "public"
            }
        ]

        response = RecognitionsResponse(
            status=StatusType.success,
            data={
                "user_id": target_id,
                "summary": {
                    "total_sent": 3,
                    "total_received": 2,
                    "points_sent": 150,
                    "points_received": 125,
                    "recognition_count_period": 5
                },
                "recognitions": recognitions,
                "analytics": {
                    "trends": {
                        "monthly_sent": [2, 3, 1, 4, 2],
                        "monthly_received": [1, 2, 2, 3, 1]
                    },
                    "top_behaviors": [
                        {
                            "behavior_name": "Exceptional Collaboration",
                            "count": 8
                        },
                        {
                            "behavior_name": "Innovation Excellence", 
                            "count": 5
                        }
                    ],
                    "frequent_collaborators": [
                        {
                            "user_id": "user2",
                            "name": "Mike Chen",
                            "interaction_count": 5
                        }
                    ]
                }
            },
            metadata={
                "total_records": len(recognitions),
                "page_info": {
                    "current_page": 1,
                    "total_pages": 1,
                    "has_next": False
                }
            }
        )
        return response.model_dump()
    except Exception as e:
        response = RecognitionsResponse(
            status=StatusType.error,
            error=ErrorDetail(code="RECOGNITIONS_ERROR", message=str(e))
        )
        return response.model_dump()

@mcp.tool(description="Provide team-level analytics and information. Args: user_id (str), tenant_id (str), context (Dict[str, Any]), filters (Optional[Dict[str, Any]]). Returns: Dict[str, Any] - TeamResponse with status, team info, team members, collaboration analytics, and recognition metrics.")
def lookup_team(
    user_id: str,
    tenant_id: str,
    context: Dict[str, Any],
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    try:
        user = mock_store.users.get(user_id)
        if not user:
            response = TeamResponse(
                status=StatusType.error,
                error=ErrorDetail(code="USER_NOT_FOUND", message="User not found")
            )
            return response.model_dump()
        
        team_name = user["role_info"]["team"]
        department = user["role_info"]["department"]
        
        # Find team members
        team_members = []
        for uid, user_data in mock_store.users.items():
            if user_data["role_info"]["team"] == team_name:
                team_members.append({
                    "user_id": uid,
                    "name": user_data["basic_info"]["name"],
                    "role": user_data["role_info"]["title"],
                    "hire_date": user_data["employment_info"]["hire_date"],
                    "recognition_stats": {
                        "points_sent": 150,
                        "points_received": 125,
                        "recognitions_sent": 3,
                        "recognitions_received": 2
                    }
                })

        data = {
            "team_info": {
                "team_id": f"team_{team_name.lower().replace(' ', '_')}",
                "team_name": team_name,
                "department": department,
                "manager_id": user["role_info"]["manager_id"],
                "manager_name": "John Smith",
                "member_count": len(team_members)
            },
            "team_members": team_members,
            "team_analytics": {
                "recognition_summary": {
                    "total_recognitions": 25,
                    "total_points_exchanged": 1250,
                    "average_recognition_value": 50,
                    "participation_rate": 0.85
                },
                "trending_behaviors": [
                    {
                        "behavior_name": "Exceptional Collaboration",
                        "frequency": 12,
                        "total_points": 600
                    },
                    {
                        "behavior_name": "Innovation Excellence",
                        "frequency": 8,
                        "total_points": 600
                    }
                ],
                "collaboration_matrix": [
                    {
                        "from_team": team_name,
                        "to_team": "Growth Team",
                        "interaction_count": 8
                    },
                    {
                        "from_team": team_name,
                        "to_team": "Design Team", 
                        "interaction_count": 5
                    }
                ],
                "top_recognizers": [
                    {
                        "user_id": "user1",
                        "name": "Sarah Johnson",
                        "recognition_count": 8
                    }
                ],
                "top_recipients": [
                    {
                        "user_id": "user2",
                        "name": "Mike Chen",
                        "points_received": 275
                    }
                ]
            }
        }
        
        response = TeamResponse(
            status=StatusType.success,
            data=data,
            metadata={
                "analysis_date": datetime.now().isoformat(),
                "data_freshness": "real_time"
            }
        )
        return response.model_dump()
    except Exception as e:
        response = TeamResponse(
            status=StatusType.error,
            error=ErrorDetail(code="TEAM_LOOKUP_ERROR", message=str(e))
        )
        return response.model_dump()

@mcp.tool(description="Aggregate recognitions for milestone cohorts and anniversary groups. Args: user_id (str), tenant_id (str), context (Dict[str, Any]), filters (Optional[Dict[str, Any]]). Returns: Dict[str, Any] - GroupRecognitionResponse with group summary, celebrants list, and department breakdown.")
def get_group_recognition(
    user_id: str,
    tenant_id: str,
    context: Dict[str, Any],
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    try:
        milestone_criteria = context.get("milestone_criteria", {})
        anniversary_years = milestone_criteria.get("anniversary_years", [5, 10, 15, 20, 25])
        
        # Generate mock celebrants
        celebrants = []
        milestone_distribution = {f"{year}_years": 0 for year in anniversary_years}
        
        # Mock celebrants data
        mock_celebrants = [
            {
                "user_id": "cel1",
                "name": "Alice Cooper",
                "title": "Senior Developer",
                "department": "Engineering",
                "hire_date": "2014-09-15",
                "anniversary_date": "2024-09-15",
                "years_of_service": 10,
                "milestone_type": "10_year"
            },
            {
                "user_id": "cel2", 
                "name": "Bob Wilson",
                "title": "Product Manager",
                "department": "Product",
                "hire_date": "2019-03-01",
                "anniversary_date": "2024-03-01",
                "years_of_service": 5,
                "milestone_type": "5_year"
            }
        ]
        
        for celebrant in mock_celebrants:
            milestone_key = f"{celebrant['years_of_service']}_years"
            if milestone_key in milestone_distribution:
                milestone_distribution[milestone_key] += 1
            
            celebrant["recognition_history"] = {
                "total_recognitions_received": 15,
                "total_points_received": 750,
                "recent_recognitions": [
                    {
                        "recognition_id": str(uuid.uuid4()),
                        "sender_name": "Team Lead",
                        "points": 75,
                        "date": (datetime.now() - timedelta(days=3)).isoformat(),
                        "message": "Congratulations on your milestone!"
                    }
                ]
            }
            celebrant["manager_info"] = {
                "manager_id": "mgr1",
                "manager_name": "Jane Manager"
            }
            celebrants.append(celebrant)

        # Department breakdown
        dept_breakdown = {}
        for celebrant in celebrants:
            dept = celebrant["department"]
            if dept not in dept_breakdown:
                dept_breakdown[dept] = {
                    "department": dept,
                    "celebrant_count": 0,
                    "milestone_breakdown": {f"{year}_years": 0 for year in anniversary_years}
                }
            dept_breakdown[dept]["celebrant_count"] += 1
            milestone_key = f"{celebrant['years_of_service']}_years"
            if milestone_key in dept_breakdown[dept]["milestone_breakdown"]:
                dept_breakdown[dept]["milestone_breakdown"][milestone_key] += 1

        response = GroupRecognitionResponse(
            status=StatusType.success,
            data={
                "group_summary": {
                    "total_celebrants": len(celebrants),
                    "milestone_distribution": milestone_distribution,
                    "period": {
                        "start_date": milestone_criteria.get("date_range", {}).get("start_date", "2024-01-01"),
                        "end_date": milestone_criteria.get("date_range", {}).get("end_date", "2024-12-31")
                    }
                },
                "celebrants": celebrants,
                "department_breakdown": list(dept_breakdown.values())
            },
            metadata={
                "query_date": datetime.now().isoformat(),
                "data_source": "hr_system"
            }
        )
        return response.model_dump()
    except Exception as e:
        response = GroupRecognitionResponse(
            status=StatusType.error,
            error=ErrorDetail(code="GROUP_RECOGNITION_ERROR", message=str(e))
        )
        return response.model_dump()

@mcp.tool(description="Create anniversary recognition entries and milestone celebrations. Args: sender_id (str), celebrant_id (str), tenant_id (str), anniversary_details (Dict[str, Any]), context (Dict[str, Any]), additional_data (Optional[Dict[str, Any]]). Returns: Dict[str, Any] - PostRecognitionResponse with recognition ID, celebration details, and notification status.")
def post_recognition(
    sender_id: str,
    celebrant_id: str,
    tenant_id: str,
    anniversary_details: Dict[str, Any],
    context: Dict[str, Any],
    additional_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    try:
        anniversary_recognition_id = str(uuid.uuid4())
        celebration_id = str(uuid.uuid4())
        
        celebrant = mock_store.users.get(celebrant_id)
        if not celebrant:
            response = PostRecognitionResponse(
                status=StatusType.error,
                error=ErrorDetail(code="CELEBRANT_NOT_FOUND", message="Celebrant not found")
            )
            return response.model_dump()
        
        milestone_years = anniversary_details["milestone_years"]
        celebrant_name = celebrant["basic_info"]["name"]

        response = PostRecognitionResponse(
            status=StatusType.success,
            data={
                "anniversary_recognition_id": anniversary_recognition_id,
                "celebration_id": celebration_id,
                "recognition_details": {
                    "celebrant_name": celebrant_name,
                    "milestone_years": milestone_years,
                    "anniversary_date": anniversary_details["anniversary_date"],
                    "recognition_message": anniversary_details["recognition_message"],
                    "created_date": datetime.now().isoformat()
                },
                "celebration_details": {
                    "celebration_type": anniversary_details["celebration_type"],
                    "visibility": "public",
                    "expected_participants": 25
                },
                "notifications_initiated": [
                    {
                        "type": "team_notification",
                        "recipient_count": 12,
                        "status": "queued"
                    },
                    {
                        "type": "manager_alert",
                        "recipient_count": 1,
                        "status": "sent"
                    },
                    {
                        "type": "public_announcement",
                        "recipient_count": 150,
                        "status": "scheduled"
                    }
                ],
                "next_steps": [
                    {
                        "action": "schedule_celebration_event",
                        "description": "Coordinate team celebration meeting",
                        "due_date": (datetime.now() + timedelta(days=7)).date().isoformat()
                    },
                    {
                        "action": "prepare_recognition_certificate",
                        "description": "Generate and deliver milestone certificate"
                    }
                ]
            },
            metadata={
                "processing_time": 250,
                "celebration_tracking_id": str(uuid.uuid4())
            }
        )
        return response.model_dump()
    except Exception as e:
        response = PostRecognitionResponse(
            status=StatusType.error,
            error=ErrorDetail(code="POST_RECOGNITION_ERROR", message=str(e))
        )
        return response.model_dump()

@mcp.tool(description="Trigger invites to colleagues for anniversary celebration events. Args: sender_id (str), celebrant_id (str), tenant_id (str), celebration_details (Dict[str, Any]), invite_criteria (Dict[str, Any]), context (Dict[str, Any]). Returns: Dict[str, Any] - CelebrationInviteResponse with invite ID, celebration details, invitee list, and RSVP tracking.")
def send_celebration_invite(
    sender_id: str,
    celebrant_id: str,
    tenant_id: str,
    celebration_details: Dict[str, Any],
    invite_criteria: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        celebrant = mock_store.users.get(celebrant_id)
        if not celebrant:
            response = CelebrationInviteResponse(
                status=StatusType.error,
                error=ErrorDetail(code="CELEBRANT_NOT_FOUND", message="Celebrant not found")
            )
            return response.model_dump()
        
        # celebration_details and invite_criteria are passed directly
        
        # Determine invitees based on criteria
        suggested_invitees = []
        invite_type = invite_criteria["invite_type"]
        
        if invite_type in ["team_only", "department", "cross_functional"]:
            for user_id, user_data in mock_store.users.items():
                if user_id != celebrant_id:  # Don't invite celebrant
                    if (invite_type == "team_only" and 
                        user_data["role_info"]["team"] == celebrant["role_info"]["team"]):
                        suggested_invitees.append(user_id)
                    elif (invite_type == "department" and 
                          user_data["role_info"]["department"] == celebrant["role_info"]["department"]):
                        suggested_invitees.append(user_id)
                    elif invite_type == "cross_functional":
                        suggested_invitees.append(user_id)
        
        # Add required attendees
        all_invitees = list(set(suggested_invitees + invite_criteria.get("required_attendees", []) + 
                                invite_criteria.get("optional_attendees", [])))
        
        # Limit based on max_invitees if specified
        max_invitees = invite_criteria.get("max_invitees")
        if max_invitees and len(all_invitees) > max_invitees:
            all_invitees = all_invitees[:max_invitees]

        response = CelebrationInviteResponse(
            status=StatusType.success,
            data={
                "celebration_invite_id": str(uuid.uuid4()),
                "celebration_details": {
                    "celebration_id": celebration_details["celebration_id"],
                    "celebrant_name": celebrant["basic_info"]["name"],
                    "milestone_years": celebration_details["milestone_years"],
                    "celebration_date": celebration_details["celebration_date"],
                    "celebration_type": celebration_details["celebration_type"],
                    "venue": celebration_details.get("venue", "Virtual Meeting Room"),
                    "duration": celebration_details.get("duration", 60)
                },
                "invite_summary": {
                    "total_invites_sent": len(all_invitees),
                    "required_attendees": len(invite_criteria.get("required_attendees", [])),
                    "optional_attendees": len(invite_criteria.get("optional_attendees", [])),
                    "auto_suggested": len(suggested_invitees)
                },
                "invitee_details": [
                    {
                        "user_id": invitee_id,
                        "name": mock_store.users.get(invitee_id, {}).get("basic_info", {}).get("name", "Unknown"),
                        "invite_type": "required" if invitee_id in invite_criteria.get("required_attendees", []) else "optional",
                        "notification_status": "sent",
                        "response_status": "pending"
                    }
                    for invitee_id in all_invitees
                ],
                "celebration_message_preview": f"Please join us in celebrating {celebrant['basic_info']['name']}'s {celebration_details['milestone_years']} year anniversary with our company!",
                "rsvp_tracking": {
                    "rsvp_deadline": (datetime.fromisoformat(celebration_details["celebration_date"]) - timedelta(days=2)).isoformat(),
                    "response_url": f"https://company.com/celebrations/{celebration_details['celebration_id']}/rsvp"
                }
            },
            metadata={
                "invite_sent_timestamp": datetime.now().isoformat(),
                "celebration_coordinator": sender_id,
                "follow_up_scheduled": (datetime.now() + timedelta(days=3)).isoformat()
            }
        )
        return response.model_dump()
    except Exception as e:
        response = CelebrationInviteResponse(
            status=StatusType.error,
            error=ErrorDetail(code="CELEBRATION_INVITE_ERROR", message=str(e))
        )
        return response.model_dump()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
