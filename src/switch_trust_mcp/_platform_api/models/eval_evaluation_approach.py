from enum import StrEnum


class EvalEvaluationApproach(StrEnum):
    METRIC = "metric"
    PROBE = "probe"

    def __str__(self) -> str:
        return str(self.value)
