import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_calendar_event(
    title: str,
    description: str,
    start_time: str,
    end_time: str,
) -> str:

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["app/mcp/calendar_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "create_calendar_event",
                arguments={
                    "title": title,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )

            if result.is_error:
                raise RuntimeError(
                    "MCP calendar tool failed."
                )

            return result.structured_content["result"]