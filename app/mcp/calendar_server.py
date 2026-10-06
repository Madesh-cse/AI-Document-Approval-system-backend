import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from mcp.server.mcpserver import MCPServer


SCOPES = ["https://www.googleapis.com/auth/calendar"]

mcp = MCPServer("Google Calendar",description="MCP server for Google Calendar integration.",)

def calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        raise RuntimeError(
            "Google Calendar authentication not found. "
            "Run test_google_calendar.py first."
        )
    return build("calendar","v3",credentials=creds,)


@mcp.tool()
def create_calendar_event(
    title: str,
    description: str,
    start_time: str,
    end_time: str,
) -> str:
    """
    Create an event in the user's primary Google Calendar.

    start_time and end_time must be ISO 8601 datetime strings.

    Example:
    2026-10-08T17:00:00+05:30
    """

    try:
        start_datetime = datetime.datetime.fromisoformat(start_time)
        end_datetime = datetime.datetime.fromisoformat(end_time)

        service = calendar_service()

        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Asia/Kolkata",
            },
        }

        created_event = (
            service.events()
            .insert(
                calendarId="primary",
                body=event,
            )
            .execute()
        )

        return (
            "Calendar event created successfully. "
            f"Event ID: {created_event['id']}"
        )

    except Exception as e:
        return f"Failed to create calendar event: {type(e).__name__}: {e}"


if __name__ == "__main__":
    mcp.run()