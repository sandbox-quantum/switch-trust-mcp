from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_link import EngineOutputLink
    from ..models.engine_output_node import EngineOutputNode


T = TypeVar("T", bound="EngineOutputSankeyResponse")


@_attrs_define
class EngineOutputSankeyResponse:
    """
    Attributes:
        cursor (str | Unset):
        links (list[EngineOutputLink] | Unset):
        nodes (list[EngineOutputNode] | Unset):
        total (int | Unset):
    """

    cursor: str | Unset = UNSET
    links: list[EngineOutputLink] | Unset = UNSET
    nodes: list[EngineOutputNode] | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_link import EngineOutputLink  # noqa: PLC0415
        from ..models.engine_output_node import EngineOutputNode  # noqa: PLC0415

        cursor = self.cursor

        links: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()
                links.append(links_item)

        nodes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = []
            for nodes_item_data in self.nodes:
                nodes_item = nodes_item_data.to_dict()
                nodes.append(nodes_item)

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if links is not UNSET:
            field_dict["links"] = links
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_link import EngineOutputLink  # noqa: PLC0415
        from ..models.engine_output_node import EngineOutputNode  # noqa: PLC0415

        d = dict(src_dict)
        cursor = d.pop("cursor", UNSET)

        _links = d.pop("links", UNSET)
        links: list[EngineOutputLink] | Unset = UNSET
        if _links is not UNSET:
            links = []
            for links_item_data in _links:
                links_item = EngineOutputLink.from_dict(links_item_data)

                links.append(links_item)

        _nodes = d.pop("nodes", UNSET)
        nodes: list[EngineOutputNode] | Unset = UNSET
        if _nodes is not UNSET:
            nodes = []
            for nodes_item_data in _nodes:
                nodes_item = EngineOutputNode.from_dict(nodes_item_data)

                nodes.append(nodes_item)

        total = d.pop("total", UNSET)

        engine_output_sankey_response = cls(
            cursor=cursor,
            links=links,
            nodes=nodes,
            total=total,
        )

        engine_output_sankey_response.additional_properties = d
        return engine_output_sankey_response

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
