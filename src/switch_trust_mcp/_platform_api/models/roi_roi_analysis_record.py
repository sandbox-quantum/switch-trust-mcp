from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.roi_roi_analysis_record_result import RoiRoiAnalysisRecordResult


T = TypeVar("T", bound="RoiRoiAnalysisRecord")


@_attrs_define
class RoiRoiAnalysisRecord:
    """
    Attributes:
        agent_id (str | Unset):
        analysis_time (str | Unset):
        analysis_type (str | Unset):
        created_at (str | Unset):
        data_watermark (str | Unset):
        error_message (str | Unset):
        estimated_savings_usd (float | Unset):
        finished_at (str | Unset):
        id (str | Unset):
        result (RoiRoiAnalysisRecordResult | Unset):
        started_at (str | Unset):
        status (str | Unset):
    """

    agent_id: str | Unset = UNSET
    analysis_time: str | Unset = UNSET
    analysis_type: str | Unset = UNSET
    created_at: str | Unset = UNSET
    data_watermark: str | Unset = UNSET
    error_message: str | Unset = UNSET
    estimated_savings_usd: float | Unset = UNSET
    finished_at: str | Unset = UNSET
    id: str | Unset = UNSET
    result: RoiRoiAnalysisRecordResult | Unset = UNSET
    started_at: str | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.roi_roi_analysis_record_result import RoiRoiAnalysisRecordResult  # noqa: PLC0415

        agent_id = self.agent_id

        analysis_time = self.analysis_time

        analysis_type = self.analysis_type

        created_at = self.created_at

        data_watermark = self.data_watermark

        error_message = self.error_message

        estimated_savings_usd = self.estimated_savings_usd

        finished_at = self.finished_at

        id = self.id

        result: dict[str, Any] | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        started_at = self.started_at

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if analysis_time is not UNSET:
            field_dict["analysis_time"] = analysis_time
        if analysis_type is not UNSET:
            field_dict["analysis_type"] = analysis_type
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if data_watermark is not UNSET:
            field_dict["data_watermark"] = data_watermark
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if estimated_savings_usd is not UNSET:
            field_dict["estimated_savings_usd"] = estimated_savings_usd
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if id is not UNSET:
            field_dict["id"] = id
        if result is not UNSET:
            field_dict["result"] = result
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.roi_roi_analysis_record_result import RoiRoiAnalysisRecordResult  # noqa: PLC0415

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        analysis_time = d.pop("analysis_time", UNSET)

        analysis_type = d.pop("analysis_type", UNSET)

        created_at = d.pop("created_at", UNSET)

        data_watermark = d.pop("data_watermark", UNSET)

        error_message = d.pop("error_message", UNSET)

        estimated_savings_usd = d.pop("estimated_savings_usd", UNSET)

        finished_at = d.pop("finished_at", UNSET)

        id = d.pop("id", UNSET)

        _result = d.pop("result", UNSET)
        result: RoiRoiAnalysisRecordResult | Unset
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = RoiRoiAnalysisRecordResult.from_dict(_result)

        started_at = d.pop("started_at", UNSET)

        status = d.pop("status", UNSET)

        roi_roi_analysis_record = cls(
            agent_id=agent_id,
            analysis_time=analysis_time,
            analysis_type=analysis_type,
            created_at=created_at,
            data_watermark=data_watermark,
            error_message=error_message,
            estimated_savings_usd=estimated_savings_usd,
            finished_at=finished_at,
            id=id,
            result=result,
            started_at=started_at,
            status=status,
        )

        roi_roi_analysis_record.additional_properties = d
        return roi_roi_analysis_record

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
