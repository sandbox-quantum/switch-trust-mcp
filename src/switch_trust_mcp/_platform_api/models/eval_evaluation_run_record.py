from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_evaluation_run_record_summary import (
        EvalEvaluationRunRecordSummary,
    )


T = TypeVar("T", bound="EvalEvaluationRunRecord")


@_attrs_define
class EvalEvaluationRunRecord:
    """
    Attributes:
        agent_evaluation_id (str | Unset):
        agent_evaluation_name (str | Unset):
        agent_id (str | Unset):
        agent_name (str | Unset):
        cancel_requested (bool | Unset):
        created_at (str | Unset):
        error_kind (str | Unset):
        error_message (str | Unset):
        finished_at (str | Unset):
        id (str | Unset):
        progress (float | Unset):
        started_at (str | Unset):
        status (str | Unset):
        summary (EvalEvaluationRunRecordSummary | Unset):
    """

    agent_evaluation_id: str | Unset = UNSET
    agent_evaluation_name: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    agent_name: str | Unset = UNSET
    cancel_requested: bool | Unset = UNSET
    created_at: str | Unset = UNSET
    error_kind: str | Unset = UNSET
    error_message: str | Unset = UNSET
    finished_at: str | Unset = UNSET
    id: str | Unset = UNSET
    progress: float | Unset = UNSET
    started_at: str | Unset = UNSET
    status: str | Unset = UNSET
    summary: EvalEvaluationRunRecordSummary | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_evaluation_run_record_summary import (
            EvalEvaluationRunRecordSummary,
        )  # noqa: PLC0415

        agent_evaluation_id = self.agent_evaluation_id

        agent_evaluation_name = self.agent_evaluation_name

        agent_id = self.agent_id

        agent_name = self.agent_name

        cancel_requested = self.cancel_requested

        created_at = self.created_at

        error_kind = self.error_kind

        error_message = self.error_message

        finished_at = self.finished_at

        id = self.id

        progress = self.progress

        started_at = self.started_at

        status = self.status

        summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_evaluation_id is not UNSET:
            field_dict["agent_evaluation_id"] = agent_evaluation_id
        if agent_evaluation_name is not UNSET:
            field_dict["agent_evaluation_name"] = agent_evaluation_name
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if agent_name is not UNSET:
            field_dict["agent_name"] = agent_name
        if cancel_requested is not UNSET:
            field_dict["cancel_requested"] = cancel_requested
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if error_kind is not UNSET:
            field_dict["error_kind"] = error_kind
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if id is not UNSET:
            field_dict["id"] = id
        if progress is not UNSET:
            field_dict["progress"] = progress
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_evaluation_run_record_summary import (
            EvalEvaluationRunRecordSummary,
        )  # noqa: PLC0415

        d = dict(src_dict)
        agent_evaluation_id = d.pop("agent_evaluation_id", UNSET)

        agent_evaluation_name = d.pop("agent_evaluation_name", UNSET)

        agent_id = d.pop("agent_id", UNSET)

        agent_name = d.pop("agent_name", UNSET)

        cancel_requested = d.pop("cancel_requested", UNSET)

        created_at = d.pop("created_at", UNSET)

        error_kind = d.pop("error_kind", UNSET)

        error_message = d.pop("error_message", UNSET)

        finished_at = d.pop("finished_at", UNSET)

        id = d.pop("id", UNSET)

        progress = d.pop("progress", UNSET)

        started_at = d.pop("started_at", UNSET)

        status = d.pop("status", UNSET)

        _summary = d.pop("summary", UNSET)
        summary: EvalEvaluationRunRecordSummary | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = EvalEvaluationRunRecordSummary.from_dict(_summary)

        eval_evaluation_run_record = cls(
            agent_evaluation_id=agent_evaluation_id,
            agent_evaluation_name=agent_evaluation_name,
            agent_id=agent_id,
            agent_name=agent_name,
            cancel_requested=cancel_requested,
            created_at=created_at,
            error_kind=error_kind,
            error_message=error_message,
            finished_at=finished_at,
            id=id,
            progress=progress,
            started_at=started_at,
            status=status,
            summary=summary,
        )

        eval_evaluation_run_record.additional_properties = d
        return eval_evaluation_run_record

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
