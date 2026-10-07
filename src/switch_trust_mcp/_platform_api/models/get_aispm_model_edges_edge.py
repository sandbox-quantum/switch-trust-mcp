from enum import StrEnum


class GetAispmModelEdgesEdge(StrEnum):
    ASSETS = "assets"
    GARAK_INFO = "garak-info"
    INSTANCES = "instances"
    ISSUES = "issues"
    LOCATIONS = "locations"
    SESSIONS = "sessions"

    def __str__(self) -> str:
        return str(self.value)
