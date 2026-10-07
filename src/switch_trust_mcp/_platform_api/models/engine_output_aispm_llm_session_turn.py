from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="EngineOutputAispmLlmSessionTurn")


@_attrs_define
class EngineOutputAispmLlmSessionTurn:
    """
    Attributes:
        cached_tokens_in (int | Unset):
        cached_tokens_out (int | Unset):
        cost (float | Unset):
        input_preview (str | Unset):
        interaction_id (str | Unset):
        prompt_guardrail_result (Any | Unset):
        response_guardrail_result (Any | Unset):
        time (str | Unset):
        tokens_in (int | Unset):
        tokens_out (int | Unset):
        total_latency_ms (int | Unset):
    """

    cached_tokens_in: int | Unset = UNSET
    cached_tokens_out: int | Unset = UNSET
    cost: float | Unset = UNSET
    input_preview: str | Unset = UNSET
    interaction_id: str | Unset = UNSET
    prompt_guardrail_result: Any | Unset = UNSET
    response_guardrail_result: Any | Unset = UNSET
    time: str | Unset = UNSET
    tokens_in: int | Unset = UNSET
    tokens_out: int | Unset = UNSET
    total_latency_ms: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cached_tokens_in = self.cached_tokens_in

        cached_tokens_out = self.cached_tokens_out

        cost = self.cost

        input_preview = self.input_preview

        interaction_id = self.interaction_id

        prompt_guardrail_result = self.prompt_guardrail_result

        response_guardrail_result = self.response_guardrail_result

        time = self.time

        tokens_in = self.tokens_in

        tokens_out = self.tokens_out

        total_latency_ms = self.total_latency_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cached_tokens_in is not UNSET:
            field_dict["cached_tokens_in"] = cached_tokens_in
        if cached_tokens_out is not UNSET:
            field_dict["cached_tokens_out"] = cached_tokens_out
        if cost is not UNSET:
            field_dict["cost"] = cost
        if input_preview is not UNSET:
            field_dict["input_preview"] = input_preview
        if interaction_id is not UNSET:
            field_dict["interaction_id"] = interaction_id
        if prompt_guardrail_result is not UNSET:
            field_dict["prompt_guardrail_result"] = prompt_guardrail_result
        if response_guardrail_result is not UNSET:
            field_dict["response_guardrail_result"] = response_guardrail_result
        if time is not UNSET:
            field_dict["time"] = time
        if tokens_in is not UNSET:
            field_dict["tokens_in"] = tokens_in
        if tokens_out is not UNSET:
            field_dict["tokens_out"] = tokens_out
        if total_latency_ms is not UNSET:
            field_dict["total_latency_ms"] = total_latency_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cached_tokens_in = d.pop("cached_tokens_in", UNSET)

        cached_tokens_out = d.pop("cached_tokens_out", UNSET)

        cost = d.pop("cost", UNSET)

        input_preview = d.pop("input_preview", UNSET)

        interaction_id = d.pop("interaction_id", UNSET)

        prompt_guardrail_result = d.pop("prompt_guardrail_result", UNSET)

        response_guardrail_result = d.pop("response_guardrail_result", UNSET)

        time = d.pop("time", UNSET)

        tokens_in = d.pop("tokens_in", UNSET)

        tokens_out = d.pop("tokens_out", UNSET)

        total_latency_ms = d.pop("total_latency_ms", UNSET)

        engine_output_aispm_llm_session_turn = cls(
            cached_tokens_in=cached_tokens_in,
            cached_tokens_out=cached_tokens_out,
            cost=cost,
            input_preview=input_preview,
            interaction_id=interaction_id,
            prompt_guardrail_result=prompt_guardrail_result,
            response_guardrail_result=response_guardrail_result,
            time=time,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            total_latency_ms=total_latency_ms,
        )

        engine_output_aispm_llm_session_turn.additional_properties = d
        return engine_output_aispm_llm_session_turn

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
