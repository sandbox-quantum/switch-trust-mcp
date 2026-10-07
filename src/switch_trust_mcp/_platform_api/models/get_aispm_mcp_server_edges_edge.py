from enum import StrEnum


class GetAispmMcpServerEdgesEdge(StrEnum):
    AISPM_MCP_PROMPTS = "aispm_mcp_prompts"
    AISPM_MCP_RESOURCES = "aispm_mcp_resources"
    AISPM_TOOLS = "aispm_tools"
    ASSETS = "assets"
    INSTANCES = "instances"
    ISSUES = "issues"
    LOCATIONS = "locations"
    SESSIONS = "sessions"

    def __str__(self) -> str:
        return str(self.value)
