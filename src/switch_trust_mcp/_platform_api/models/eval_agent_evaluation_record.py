from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.eval_agent_evaluation_record_schedule import (
    EvalAgentEvaluationRecordSchedule,
)
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_evaluation_record_config import (
        EvalAgentEvaluationRecordConfig,
    )
    from ..models.eval_agent_evaluation_record_latest_run_summary import (
        EvalAgentEvaluationRecordLatestRunSummary,
    )
    from ..models.eval_agent_evaluation_record_latest_scored_run_summary import (
        EvalAgentEvaluationRecordLatestScoredRunSummary,
    )


T = TypeVar("T", bound="EvalAgentEvaluationRecord")


@_attrs_define
class EvalAgentEvaluationRecord:
    """
    Attributes:
        agent_id (str | Unset):
        config (EvalAgentEvaluationRecordConfig | Unset):
        created_at (str | Unset):
        evaluation_id (str | Unset):
        evaluation_name (str | Unset):
        id (str | Unset):
        latest_run_cancel_requested (bool | Unset):
        latest_run_finished_at (str | Unset):
        latest_run_id (str | Unset):
        latest_run_progress (float | Unset):
        latest_run_started_at (str | Unset):
        latest_run_status (str | Unset):
        latest_run_summary (EvalAgentEvaluationRecordLatestRunSummary | Unset):
        latest_scored_run_finished_at (str | Unset):
        latest_scored_run_id (str | Unset):
        latest_scored_run_summary (EvalAgentEvaluationRecordLatestScoredRunSummary | Unset):
        name (str | Unset):
        run_requested (bool | Unset):
        schedule (EvalAgentEvaluationRecordSchedule | Unset):
        score_trend (list[float] | Unset):
        updated_at (str | Unset):
        weight (float | Unset):
    """

    agent_id: str | Unset = UNSET
    config: EvalAgentEvaluationRecordConfig | Unset = UNSET
    created_at: str | Unset = UNSET
    evaluation_id: str | Unset = UNSET
    evaluation_name: str | Unset = UNSET
    id: str | Unset = UNSET
    latest_run_cancel_requested: bool | Unset = UNSET
    latest_run_finished_at: str | Unset = UNSET
    latest_run_id: str | Unset = UNSET
    latest_run_progress: float | Unset = UNSET
    latest_run_started_at: str | Unset = UNSET
    latest_run_status: str | Unset = UNSET
    latest_run_summary: EvalAgentEvaluationRecordLatestRunSummary | Unset = UNSET
    latest_scored_run_finished_at: str | Unset = UNSET
    latest_scored_run_id: str | Unset = UNSET
    latest_scored_run_summary: (
        EvalAgentEvaluationRecordLatestScoredRunSummary | Unset
    ) = UNSET
    name: str | Unset = UNSET
    run_requested: bool | Unset = UNSET
    schedule: EvalAgentEvaluationRecordSchedule | Unset = UNSET
    score_trend: list[float] | Unset = UNSET
    updated_at: str | Unset = UNSET
    weight: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_evaluation_record_config import (
            EvalAgentEvaluationRecordConfig,
        )  # noqa: PLC0415
        from ..models.eval_agent_evaluation_record_latest_run_summary import (
            EvalAgentEvaluationRecordLatestRunSummary,
        )  # noqa: PLC0415
        from ..models.eval_agent_evaluation_record_latest_scored_run_summary import (
            EvalAgentEvaluationRecordLatestScoredRunSummary,
        )  # noqa: PLC0415

        agent_id = self.agent_id

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at = self.created_at

        evaluation_id = self.evaluation_id

        evaluation_name = self.evaluation_name

        id = self.id

        latest_run_cancel_requested = self.latest_run_cancel_requested

        latest_run_finished_at = self.latest_run_finished_at

        latest_run_id = self.latest_run_id

        latest_run_progress = self.latest_run_progress

        latest_run_started_at = self.latest_run_started_at

        latest_run_status = self.latest_run_status

        latest_run_summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.latest_run_summary, Unset):
            latest_run_summary = self.latest_run_summary.to_dict()

        latest_scored_run_finished_at = self.latest_scored_run_finished_at

        latest_scored_run_id = self.latest_scored_run_id

        latest_scored_run_summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.latest_scored_run_summary, Unset):
            latest_scored_run_summary = self.latest_scored_run_summary.to_dict()

        name = self.name

        run_requested = self.run_requested

        schedule: str | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.value

        score_trend: list[float] | Unset = UNSET
        if not isinstance(self.score_trend, Unset):
            score_trend = self.score_trend

        updated_at = self.updated_at

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if evaluation_name is not UNSET:
            field_dict["evaluation_name"] = evaluation_name
        if id is not UNSET:
            field_dict["id"] = id
        if latest_run_cancel_requested is not UNSET:
            field_dict["latest_run_cancel_requested"] = latest_run_cancel_requested
        if latest_run_finished_at is not UNSET:
            field_dict["latest_run_finished_at"] = latest_run_finished_at
        if latest_run_id is not UNSET:
            field_dict["latest_run_id"] = latest_run_id
        if latest_run_progress is not UNSET:
            field_dict["latest_run_progress"] = latest_run_progress
        if latest_run_started_at is not UNSET:
            field_dict["latest_run_started_at"] = latest_run_started_at
        if latest_run_status is not UNSET:
            field_dict["latest_run_status"] = latest_run_status
        if latest_run_summary is not UNSET:
            field_dict["latest_run_summary"] = latest_run_summary
        if latest_scored_run_finished_at is not UNSET:
            field_dict["latest_scored_run_finished_at"] = latest_scored_run_finished_at
        if latest_scored_run_id is not UNSET:
            field_dict["latest_scored_run_id"] = latest_scored_run_id
        if latest_scored_run_summary is not UNSET:
            field_dict["latest_scored_run_summary"] = latest_scored_run_summary
        if name is not UNSET:
            field_dict["name"] = name
        if run_requested is not UNSET:
            field_dict["run_requested"] = run_requested
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if score_trend is not UNSET:
            field_dict["score_trend"] = score_trend
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_evaluation_record_config import (
            EvalAgentEvaluationRecordConfig,
        )  # noqa: PLC0415
        from ..models.eval_agent_evaluation_record_latest_run_summary import (
            EvalAgentEvaluationRecordLatestRunSummary,
        )  # noqa: PLC0415
        from ..models.eval_agent_evaluation_record_latest_scored_run_summary import (
            EvalAgentEvaluationRecordLatestScoredRunSummary,
        )  # noqa: PLC0415

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        _config = d.pop("config", UNSET)
        config: EvalAgentEvaluationRecordConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalAgentEvaluationRecordConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        evaluation_id = d.pop("evaluation_id", UNSET)

        evaluation_name = d.pop("evaluation_name", UNSET)

        id = d.pop("id", UNSET)

        latest_run_cancel_requested = d.pop("latest_run_cancel_requested", UNSET)

        latest_run_finished_at = d.pop("latest_run_finished_at", UNSET)

        latest_run_id = d.pop("latest_run_id", UNSET)

        latest_run_progress = d.pop("latest_run_progress", UNSET)

        latest_run_started_at = d.pop("latest_run_started_at", UNSET)

        latest_run_status = d.pop("latest_run_status", UNSET)

        _latest_run_summary = d.pop("latest_run_summary", UNSET)
        latest_run_summary: EvalAgentEvaluationRecordLatestRunSummary | Unset
        if isinstance(_latest_run_summary, Unset):
            latest_run_summary = UNSET
        else:
            latest_run_summary = EvalAgentEvaluationRecordLatestRunSummary.from_dict(
                _latest_run_summary
            )

        latest_scored_run_finished_at = d.pop("latest_scored_run_finished_at", UNSET)

        latest_scored_run_id = d.pop("latest_scored_run_id", UNSET)

        _latest_scored_run_summary = d.pop("latest_scored_run_summary", UNSET)
        latest_scored_run_summary: (
            EvalAgentEvaluationRecordLatestScoredRunSummary | Unset
        )
        if isinstance(_latest_scored_run_summary, Unset):
            latest_scored_run_summary = UNSET
        else:
            latest_scored_run_summary = (
                EvalAgentEvaluationRecordLatestScoredRunSummary.from_dict(
                    _latest_scored_run_summary
                )
            )

        name = d.pop("name", UNSET)

        run_requested = d.pop("run_requested", UNSET)

        _schedule = d.pop("schedule", UNSET)
        schedule: EvalAgentEvaluationRecordSchedule | Unset
        if isinstance(_schedule, Unset):
            schedule = UNSET
        else:
            schedule = EvalAgentEvaluationRecordSchedule(_schedule)

        score_trend = cast(list[float], d.pop("score_trend", UNSET))

        updated_at = d.pop("updated_at", UNSET)

        weight = d.pop("weight", UNSET)

        eval_agent_evaluation_record = cls(
            agent_id=agent_id,
            config=config,
            created_at=created_at,
            evaluation_id=evaluation_id,
            evaluation_name=evaluation_name,
            id=id,
            latest_run_cancel_requested=latest_run_cancel_requested,
            latest_run_finished_at=latest_run_finished_at,
            latest_run_id=latest_run_id,
            latest_run_progress=latest_run_progress,
            latest_run_started_at=latest_run_started_at,
            latest_run_status=latest_run_status,
            latest_run_summary=latest_run_summary,
            latest_scored_run_finished_at=latest_scored_run_finished_at,
            latest_scored_run_id=latest_scored_run_id,
            latest_scored_run_summary=latest_scored_run_summary,
            name=name,
            run_requested=run_requested,
            schedule=schedule,
            score_trend=score_trend,
            updated_at=updated_at,
            weight=weight,
        )

        eval_agent_evaluation_record.additional_properties = d
        return eval_agent_evaluation_record

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
