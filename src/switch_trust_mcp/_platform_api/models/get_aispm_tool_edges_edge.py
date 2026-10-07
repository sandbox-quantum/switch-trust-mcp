from enum import StrEnum


class GetAispmToolEdgesEdge(StrEnum):
    AGENTS = "agents"
    ISSUES = "issues"
    LOCATIONS = "locations"
    MCP_SERVERS = "mcp_servers"

    def __str__(self) -> str:
        return str(self.value)
