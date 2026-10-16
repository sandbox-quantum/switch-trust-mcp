from enum import StrEnum


class CostModelPricingSource(StrEnum):
    CUSTOM = "custom"
    PLATFORM = "platform"
    UNPRICED = "unpriced"

    def __str__(self) -> str:
        return str(self.value)
