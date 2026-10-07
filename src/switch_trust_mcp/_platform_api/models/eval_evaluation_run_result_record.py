from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_evaluation_run_result_record_conversation import (
        EvalEvaluationRunResultRecordConversation,
    )


T = TypeVar("T", bound="EvalEvaluationRunResultRecord")


@_attrs_define
class EvalEvaluationRunResultRecord:
    """
    Attributes:
        conversation (EvalEvaluationRunResultRecordConversation | Unset):
        created_at (str | Unset):
        error_message (str | Unset):
        evaluation_run_id (str | Unset):
        id (str | Unset):
        score (float | Unset):
        status (str | Unset):
    """

    conversation: EvalEvaluationRunResultRecordConversation | Unset = UNSET
    created_at: str | Unset = UNSET
    error_message: str | Unset = UNSET
    evaluation_run_id: str | Unset = UNSET
    id: str | Unset = UNSET
    score: float | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_evaluation_run_result_record_conversation import (
            EvalEvaluationRunResultRecordConversation,
        )  # noqa: PLC0415

        conversation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conversation, Unset):
            conversation = self.conversation.to_dict()

        created_at = self.created_at

        error_message = self.error_message

        evaluation_run_id = self.evaluation_run_id

        id = self.id

        score = self.score

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conversation is not UNSET:
            field_dict["conversation"] = conversation
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if evaluation_run_id is not UNSET:
            field_dict["evaluation_run_id"] = evaluation_run_id
        if id is not UNSET:
            field_dict["id"] = id
        if score is not UNSET:
            field_dict["score"] = score
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_evaluation_run_result_record_conversation import (
            EvalEvaluationRunResultRecordConversation,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _conversation = d.pop("conversation", UNSET)
        conversation: EvalEvaluationRunResultRecordConversation | Unset
        if isinstance(_conversation, Unset):
            conversation = UNSET
        else:
            conversation = EvalEvaluationRunResultRecordConversation.from_dict(
                _conversation
            )

        created_at = d.pop("created_at", UNSET)

        error_message = d.pop("error_message", UNSET)

        evaluation_run_id = d.pop("evaluation_run_id", UNSET)

        id = d.pop("id", UNSET)

        score = d.pop("score", UNSET)

        status = d.pop("status", UNSET)

        eval_evaluation_run_result_record = cls(
            conversation=conversation,
            created_at=created_at,
            error_message=error_message,
            evaluation_run_id=evaluation_run_id,
            id=id,
            score=score,
            status=status,
        )

        eval_evaluation_run_result_record.additional_properties = d
        return eval_evaluation_run_result_record

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
