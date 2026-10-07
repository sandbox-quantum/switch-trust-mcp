from enum import StrEnum


class GetAispmAgentEdgesEdge(StrEnum):
    AISPM_AGENT_DEPENDENCIES = "aispm_agent_dependencies"
    AISPM_INPUT_GUARDRAILS = "aispm_input_guardrails"
    AISPM_MCP_SERVER_DEPENDENCIES = "aispm_mcp_server_dependencies"
    AISPM_MODEL_DEPENDENCIES = "aispm_model_dependencies"
    AISPM_OUTPUT_GUARDRAILS = "aispm_output_guardrails"
    AISPM_TOOLS = "aispm_tools"
    ASSETS = "assets"
    INSTANCES = "instances"
    ISSUES = "issues"
    LOCATIONS = "locations"
    SESSIONS = "sessions"

    def __str__(self) -> str:
        return str(self.value)
