from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.eval_evaluation_record_approach import EvalEvaluationRecordApproach
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_evaluation_record_config import EvalEvaluationRecordConfig
    from ..models.eval_evaluation_record_tags import EvalEvaluationRecordTags


T = TypeVar("T", bound="EvalEvaluationRecord")


@_attrs_define
class EvalEvaluationRecord:
    """
    Attributes:
        approach (EvalEvaluationRecordApproach | Unset):
        config (EvalEvaluationRecordConfig | Unset):
        created_at (str | Unset):
        description (str | Unset):
        id (str | Unset):
        is_builtin (bool | Unset):
        name (str | Unset):
        num_prompts (int | Unset):
        tags (EvalEvaluationRecordTags | Unset):
        type_ (str | Unset):
        updated_at (str | Unset):
    """

    approach: EvalEvaluationRecordApproach | Unset = UNSET
    config: EvalEvaluationRecordConfig | Unset = UNSET
    created_at: str | Unset = UNSET
    description: str | Unset = UNSET
    id: str | Unset = UNSET
    is_builtin: bool | Unset = UNSET
    name: str | Unset = UNSET
    num_prompts: int | Unset = UNSET
    tags: EvalEvaluationRecordTags | Unset = UNSET
    type_: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_evaluation_record_config import EvalEvaluationRecordConfig  # noqa: PLC0415
        from ..models.eval_evaluation_record_tags import EvalEvaluationRecordTags  # noqa: PLC0415

        approach: str | Unset = UNSET
        if not isinstance(self.approach, Unset):
            approach = self.approach.value

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at = self.created_at

        description = self.description

        id = self.id

        is_builtin = self.is_builtin

        name = self.name

        num_prompts = self.num_prompts

        tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        type_ = self.type_

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approach is not UNSET:
            field_dict["approach"] = approach
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if is_builtin is not UNSET:
            field_dict["is_builtin"] = is_builtin
        if name is not UNSET:
            field_dict["name"] = name
        if num_prompts is not UNSET:
            field_dict["num_prompts"] = num_prompts
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_evaluation_record_config import EvalEvaluationRecordConfig  # noqa: PLC0415
        from ..models.eval_evaluation_record_tags import EvalEvaluationRecordTags  # noqa: PLC0415

        d = dict(src_dict)
        _approach = d.pop("approach", UNSET)
        approach: EvalEvaluationRecordApproach | Unset
        if isinstance(_approach, Unset):
            approach = UNSET
        else:
            approach = EvalEvaluationRecordApproach(_approach)

        _config = d.pop("config", UNSET)
        config: EvalEvaluationRecordConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalEvaluationRecordConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        is_builtin = d.pop("is_builtin", UNSET)

        name = d.pop("name", UNSET)

        num_prompts = d.pop("num_prompts", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: EvalEvaluationRecordTags | Unset
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = EvalEvaluationRecordTags.from_dict(_tags)

        type_ = d.pop("type", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        eval_evaluation_record = cls(
            approach=approach,
            config=config,
            created_at=created_at,
            description=description,
            id=id,
            is_builtin=is_builtin,
            name=name,
            num_prompts=num_prompts,
            tags=tags,
            type_=type_,
            updated_at=updated_at,
        )

        eval_evaluation_record.additional_properties = d
        return eval_evaluation_record

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
