from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.eval_agent_evaluation_schedule import EvalAgentEvaluationSchedule
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_evaluation_config import EvalAgentEvaluationConfig


T = TypeVar("T", bound="EvalAgentEvaluation")


@_attrs_define
class EvalAgentEvaluation:
    """
    Attributes:
        agent_id (str | Unset):
        config (EvalAgentEvaluationConfig | Unset):
        evaluation_id (str | Unset):
        name (str | Unset):
        schedule (EvalAgentEvaluationSchedule | Unset):
        weight (float | Unset):
    """

    agent_id: str | Unset = UNSET
    config: EvalAgentEvaluationConfig | Unset = UNSET
    evaluation_id: str | Unset = UNSET
    name: str | Unset = UNSET
    schedule: EvalAgentEvaluationSchedule | Unset = UNSET
    weight: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_evaluation_config import EvalAgentEvaluationConfig  # noqa: PLC0415

        agent_id = self.agent_id

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        evaluation_id = self.evaluation_id

        name = self.name

        schedule: str | Unset = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.value

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if config is not UNSET:
            field_dict["config"] = config
        if evaluation_id is not UNSET:
            field_dict["evaluation_id"] = evaluation_id
        if name is not UNSET:
            field_dict["name"] = name
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_evaluation_config import EvalAgentEvaluationConfig  # noqa: PLC0415

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        _config = d.pop("config", UNSET)
        config: EvalAgentEvaluationConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalAgentEvaluationConfig.from_dict(_config)

        evaluation_id = d.pop("evaluation_id", UNSET)

        name = d.pop("name", UNSET)

        _schedule = d.pop("schedule", UNSET)
        schedule: EvalAgentEvaluationSchedule | Unset
        if isinstance(_schedule, Unset):
            schedule = UNSET
        else:
            schedule = EvalAgentEvaluationSchedule(_schedule)

        weight = d.pop("weight", UNSET)

        eval_agent_evaluation = cls(
            agent_id=agent_id,
            config=config,
            evaluation_id=evaluation_id,
            name=name,
            schedule=schedule,
            weight=weight,
        )

        eval_agent_evaluation.additional_properties = d
        return eval_agent_evaluation

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
