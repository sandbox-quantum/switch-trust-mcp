from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_aispm_llm_session_turn import (
        EngineOutputAispmLlmSessionTurn,
    )


T = TypeVar("T", bound="EngineOutputAispmLlmSessionDetail")


@_attrs_define
class EngineOutputAispmLlmSessionDetail:
    """
    Attributes:
        agent_name (str | Unset):
        cost (float | Unset):
        duration_ms (float | Unset):
        prompt_guardrail_result (Any | Unset):
        response_guardrail_result (Any | Unset):
        session_id (str | Unset):
        time (str | Unset):
        tokens (int | Unset):
        turns (int | Unset):
        turns_list (list[EngineOutputAispmLlmSessionTurn] | Unset):
    """

    agent_name: str | Unset = UNSET
    cost: float | Unset = UNSET
    duration_ms: float | Unset = UNSET
    prompt_guardrail_result: Any | Unset = UNSET
    response_guardrail_result: Any | Unset = UNSET
    session_id: str | Unset = UNSET
    time: str | Unset = UNSET
    tokens: int | Unset = UNSET
    turns: int | Unset = UNSET
    turns_list: list[EngineOutputAispmLlmSessionTurn] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_aispm_llm_session_turn import (
            EngineOutputAispmLlmSessionTurn,
        )  # noqa: PLC0415

        agent_name = self.agent_name

        cost = self.cost

        duration_ms = self.duration_ms

        prompt_guardrail_result = self.prompt_guardrail_result

        response_guardrail_result = self.response_guardrail_result

        session_id = self.session_id

        time = self.time

        tokens = self.tokens

        turns = self.turns

        turns_list: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.turns_list, Unset):
            turns_list = []
            for turns_list_item_data in self.turns_list:
                turns_list_item = turns_list_item_data.to_dict()
                turns_list.append(turns_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_name is not UNSET:
            field_dict["agent_name"] = agent_name
        if cost is not UNSET:
            field_dict["cost"] = cost
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if prompt_guardrail_result is not UNSET:
            field_dict["prompt_guardrail_result"] = prompt_guardrail_result
        if response_guardrail_result is not UNSET:
            field_dict["response_guardrail_result"] = response_guardrail_result
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if time is not UNSET:
            field_dict["time"] = time
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if turns is not UNSET:
            field_dict["turns"] = turns
        if turns_list is not UNSET:
            field_dict["turns_list"] = turns_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_aispm_llm_session_turn import (
            EngineOutputAispmLlmSessionTurn,
        )  # noqa: PLC0415

        d = dict(src_dict)
        agent_name = d.pop("agent_name", UNSET)

        cost = d.pop("cost", UNSET)

        duration_ms = d.pop("duration_ms", UNSET)

        prompt_guardrail_result = d.pop("prompt_guardrail_result", UNSET)

        response_guardrail_result = d.pop("response_guardrail_result", UNSET)

        session_id = d.pop("session_id", UNSET)

        time = d.pop("time", UNSET)

        tokens = d.pop("tokens", UNSET)

        turns = d.pop("turns", UNSET)

        _turns_list = d.pop("turns_list", UNSET)
        turns_list: list[EngineOutputAispmLlmSessionTurn] | Unset = UNSET
        if _turns_list is not UNSET:
            turns_list = []
            for turns_list_item_data in _turns_list:
                turns_list_item = EngineOutputAispmLlmSessionTurn.from_dict(
                    turns_list_item_data
                )

                turns_list.append(turns_list_item)

        engine_output_aispm_llm_session_detail = cls(
            agent_name=agent_name,
            cost=cost,
            duration_ms=duration_ms,
            prompt_guardrail_result=prompt_guardrail_result,
            response_guardrail_result=response_guardrail_result,
            session_id=session_id,
            time=time,
            tokens=tokens,
            turns=turns,
            turns_list=turns_list,
        )

        engine_output_aispm_llm_session_detail.additional_properties = d
        return engine_output_aispm_llm_session_detail

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
