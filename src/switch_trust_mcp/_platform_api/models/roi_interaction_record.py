from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.roi_interaction_record_tool_definitions import (
        RoiInteractionRecordToolDefinitions,
    )
    from ..models.roi_interaction_record_tool_use import RoiInteractionRecordToolUse


T = TypeVar("T", bound="RoiInteractionRecord")


@_attrs_define
class RoiInteractionRecord:
    """
    Attributes:
        agent_id (str | Unset):
        cache_read_tokens (int | Unset):
        cache_write_tokens (int | Unset):
        cost_usd (float | Unset):
        guardrail_result_prompt (str | Unset):
        guardrail_result_response (str | Unset):
        id (str | Unset):
        input_tokens (int | Unset):
        interaction_time (str | Unset):
        max_tokens (int | Unset):
        model_fingerprint (str | Unset):
        model_latency_ms (int | Unset):
        model_name (str | Unset):
        model_supplier (str | Unset):
        output_tokens (int | Unset):
        prompt_text (str | Unset):
        response_text (str | Unset):
        session_id (str | Unset):
        stop_reason (str | Unset):
        tool_definitions (RoiInteractionRecordToolDefinitions | Unset):
        tool_use (RoiInteractionRecordToolUse | Unset):
        total_latency_ms (int | Unset):
    """

    agent_id: str | Unset = UNSET
    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    cost_usd: float | Unset = UNSET
    guardrail_result_prompt: str | Unset = UNSET
    guardrail_result_response: str | Unset = UNSET
    id: str | Unset = UNSET
    input_tokens: int | Unset = UNSET
    interaction_time: str | Unset = UNSET
    max_tokens: int | Unset = UNSET
    model_fingerprint: str | Unset = UNSET
    model_latency_ms: int | Unset = UNSET
    model_name: str | Unset = UNSET
    model_supplier: str | Unset = UNSET
    output_tokens: int | Unset = UNSET
    prompt_text: str | Unset = UNSET
    response_text: str | Unset = UNSET
    session_id: str | Unset = UNSET
    stop_reason: str | Unset = UNSET
    tool_definitions: RoiInteractionRecordToolDefinitions | Unset = UNSET
    tool_use: RoiInteractionRecordToolUse | Unset = UNSET
    total_latency_ms: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.roi_interaction_record_tool_definitions import (
            RoiInteractionRecordToolDefinitions,
        )  # noqa: PLC0415
        from ..models.roi_interaction_record_tool_use import RoiInteractionRecordToolUse  # noqa: PLC0415

        agent_id = self.agent_id

        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        cost_usd = self.cost_usd

        guardrail_result_prompt = self.guardrail_result_prompt

        guardrail_result_response = self.guardrail_result_response

        id = self.id

        input_tokens = self.input_tokens

        interaction_time = self.interaction_time

        max_tokens = self.max_tokens

        model_fingerprint = self.model_fingerprint

        model_latency_ms = self.model_latency_ms

        model_name = self.model_name

        model_supplier = self.model_supplier

        output_tokens = self.output_tokens

        prompt_text = self.prompt_text

        response_text = self.response_text

        session_id = self.session_id

        stop_reason = self.stop_reason

        tool_definitions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tool_definitions, Unset):
            tool_definitions = self.tool_definitions.to_dict()

        tool_use: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tool_use, Unset):
            tool_use = self.tool_use.to_dict()

        total_latency_ms = self.total_latency_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if cost_usd is not UNSET:
            field_dict["cost_usd"] = cost_usd
        if guardrail_result_prompt is not UNSET:
            field_dict["guardrail_result_prompt"] = guardrail_result_prompt
        if guardrail_result_response is not UNSET:
            field_dict["guardrail_result_response"] = guardrail_result_response
        if id is not UNSET:
            field_dict["id"] = id
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if interaction_time is not UNSET:
            field_dict["interaction_time"] = interaction_time
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if model_fingerprint is not UNSET:
            field_dict["model_fingerprint"] = model_fingerprint
        if model_latency_ms is not UNSET:
            field_dict["model_latency_ms"] = model_latency_ms
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_supplier is not UNSET:
            field_dict["model_supplier"] = model_supplier
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if prompt_text is not UNSET:
            field_dict["prompt_text"] = prompt_text
        if response_text is not UNSET:
            field_dict["response_text"] = response_text
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if tool_definitions is not UNSET:
            field_dict["tool_definitions"] = tool_definitions
        if tool_use is not UNSET:
            field_dict["tool_use"] = tool_use
        if total_latency_ms is not UNSET:
            field_dict["total_latency_ms"] = total_latency_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.roi_interaction_record_tool_definitions import (
            RoiInteractionRecordToolDefinitions,
        )  # noqa: PLC0415
        from ..models.roi_interaction_record_tool_use import RoiInteractionRecordToolUse  # noqa: PLC0415

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        cost_usd = d.pop("cost_usd", UNSET)

        guardrail_result_prompt = d.pop("guardrail_result_prompt", UNSET)

        guardrail_result_response = d.pop("guardrail_result_response", UNSET)

        id = d.pop("id", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        interaction_time = d.pop("interaction_time", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        model_fingerprint = d.pop("model_fingerprint", UNSET)

        model_latency_ms = d.pop("model_latency_ms", UNSET)

        model_name = d.pop("model_name", UNSET)

        model_supplier = d.pop("model_supplier", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        prompt_text = d.pop("prompt_text", UNSET)

        response_text = d.pop("response_text", UNSET)

        session_id = d.pop("session_id", UNSET)

        stop_reason = d.pop("stop_reason", UNSET)

        _tool_definitions = d.pop("tool_definitions", UNSET)
        tool_definitions: RoiInteractionRecordToolDefinitions | Unset
        if isinstance(_tool_definitions, Unset):
            tool_definitions = UNSET
        else:
            tool_definitions = RoiInteractionRecordToolDefinitions.from_dict(
                _tool_definitions
            )

        _tool_use = d.pop("tool_use", UNSET)
        tool_use: RoiInteractionRecordToolUse | Unset
        if isinstance(_tool_use, Unset):
            tool_use = UNSET
        else:
            tool_use = RoiInteractionRecordToolUse.from_dict(_tool_use)

        total_latency_ms = d.pop("total_latency_ms", UNSET)

        roi_interaction_record = cls(
            agent_id=agent_id,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            cost_usd=cost_usd,
            guardrail_result_prompt=guardrail_result_prompt,
            guardrail_result_response=guardrail_result_response,
            id=id,
            input_tokens=input_tokens,
            interaction_time=interaction_time,
            max_tokens=max_tokens,
            model_fingerprint=model_fingerprint,
            model_latency_ms=model_latency_ms,
            model_name=model_name,
            model_supplier=model_supplier,
            output_tokens=output_tokens,
            prompt_text=prompt_text,
            response_text=response_text,
            session_id=session_id,
            stop_reason=stop_reason,
            tool_definitions=tool_definitions,
            tool_use=tool_use,
            total_latency_ms=total_latency_ms,
        )

        roi_interaction_record.additional_properties = d
        return roi_interaction_record

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
