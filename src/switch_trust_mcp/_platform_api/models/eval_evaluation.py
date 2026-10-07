from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.eval_evaluation_approach import EvalEvaluationApproach
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_evaluation_config import EvalEvaluationConfig
    from ..models.eval_evaluation_tags import EvalEvaluationTags


T = TypeVar("T", bound="EvalEvaluation")


@_attrs_define
class EvalEvaluation:
    """
    Attributes:
        approach (EvalEvaluationApproach | Unset):
        config (EvalEvaluationConfig | Unset):
        description (str | Unset):
        name (str | Unset):
        tags (EvalEvaluationTags | Unset):
        type_ (str | Unset):
    """

    approach: EvalEvaluationApproach | Unset = UNSET
    config: EvalEvaluationConfig | Unset = UNSET
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    tags: EvalEvaluationTags | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_evaluation_config import EvalEvaluationConfig  # noqa: PLC0415
        from ..models.eval_evaluation_tags import EvalEvaluationTags  # noqa: PLC0415

        approach: str | Unset = UNSET
        if not isinstance(self.approach, Unset):
            approach = self.approach.value

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        description = self.description

        name = self.name

        tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approach is not UNSET:
            field_dict["approach"] = approach
        if config is not UNSET:
            field_dict["config"] = config
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_evaluation_config import EvalEvaluationConfig  # noqa: PLC0415
        from ..models.eval_evaluation_tags import EvalEvaluationTags  # noqa: PLC0415

        d = dict(src_dict)
        _approach = d.pop("approach", UNSET)
        approach: EvalEvaluationApproach | Unset
        if isinstance(_approach, Unset):
            approach = UNSET
        else:
            approach = EvalEvaluationApproach(_approach)

        _config = d.pop("config", UNSET)
        config: EvalEvaluationConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalEvaluationConfig.from_dict(_config)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: EvalEvaluationTags | Unset
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = EvalEvaluationTags.from_dict(_tags)

        type_ = d.pop("type", UNSET)

        eval_evaluation = cls(
            approach=approach,
            config=config,
            description=description,
            name=name,
            tags=tags,
            type_=type_,
        )

        eval_evaluation.additional_properties = d
        return eval_evaluation

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
