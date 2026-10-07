from enum import StrEnum


class EvalEvaluationRecordApproach(StrEnum):
    METRIC = "metric"
    PROBE = "probe"

    def __str__(self) -> str:
        return str(self.value)
