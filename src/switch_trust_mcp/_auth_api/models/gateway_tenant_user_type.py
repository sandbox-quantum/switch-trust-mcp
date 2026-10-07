from enum import StrEnum


class GatewayTenantUserType(StrEnum):
    TENANT_USER_INVITATION = "invitation"
    TENANT_USER_MEMBER = "member"

    def __str__(self) -> str:
        return str(self.value)
