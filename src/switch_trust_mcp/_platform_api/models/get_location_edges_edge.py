from enum import StrEnum


class GetLocationEdgesEdge(StrEnum):
    CERTS = "certs"
    QUALYS_SECRETS = "qualys-secrets"
    SECRETS = "secrets"

    def __str__(self) -> str:
        return str(self.value)
