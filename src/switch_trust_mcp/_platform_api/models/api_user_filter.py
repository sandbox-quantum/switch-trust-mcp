from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.api_include_exclude import ApiIncludeExclude
    from ..models.api_user_filter_tags_item import ApiUserFilterTagsItem


T = TypeVar("T", bound="ApiUserFilter")


@_attrs_define
class ApiUserFilter:
    """
    Attributes:
        application (ApiIncludeExclude | Unset):
        distribution (ApiIncludeExclude | Unset):
        known (ApiIncludeExclude | Unset):
        last_seen (str | Unset):
        package (ApiIncludeExclude | Unset):
        path (ApiIncludeExclude | Unset):
        profiles (list[str] | Unset):
        severities (list[str] | Unset):
        show_excluded (bool | Unset):
        sources (list[str] | Unset):
        tags (list[ApiUserFilterTagsItem] | Unset):
    """

    application: ApiIncludeExclude | Unset = UNSET
    distribution: ApiIncludeExclude | Unset = UNSET
    known: ApiIncludeExclude | Unset = UNSET
    last_seen: str | Unset = UNSET
    package: ApiIncludeExclude | Unset = UNSET
    path: ApiIncludeExclude | Unset = UNSET
    profiles: list[str] | Unset = UNSET
    severities: list[str] | Unset = UNSET
    show_excluded: bool | Unset = UNSET
    sources: list[str] | Unset = UNSET
    tags: list[ApiUserFilterTagsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_include_exclude import ApiIncludeExclude  # noqa: PLC0415
        from ..models.api_user_filter_tags_item import ApiUserFilterTagsItem  # noqa: PLC0415

        application: dict[str, Any] | Unset = UNSET
        if not isinstance(self.application, Unset):
            application = self.application.to_dict()

        distribution: dict[str, Any] | Unset = UNSET
        if not isinstance(self.distribution, Unset):
            distribution = self.distribution.to_dict()

        known: dict[str, Any] | Unset = UNSET
        if not isinstance(self.known, Unset):
            known = self.known.to_dict()

        last_seen = self.last_seen

        package: dict[str, Any] | Unset = UNSET
        if not isinstance(self.package, Unset):
            package = self.package.to_dict()

        path: dict[str, Any] | Unset = UNSET
        if not isinstance(self.path, Unset):
            path = self.path.to_dict()

        profiles: list[str] | Unset = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles

        severities: list[str] | Unset = UNSET
        if not isinstance(self.severities, Unset):
            severities = self.severities

        show_excluded = self.show_excluded

        sources: list[str] | Unset = UNSET
        if not isinstance(self.sources, Unset):
            sources = self.sources

        tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if application is not UNSET:
            field_dict["application"] = application
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if known is not UNSET:
            field_dict["known"] = known
        if last_seen is not UNSET:
            field_dict["lastSeen"] = last_seen
        if package is not UNSET:
            field_dict["package"] = package
        if path is not UNSET:
            field_dict["path"] = path
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if severities is not UNSET:
            field_dict["severities"] = severities
        if show_excluded is not UNSET:
            field_dict["showExcluded"] = show_excluded
        if sources is not UNSET:
            field_dict["sources"] = sources
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_include_exclude import ApiIncludeExclude  # noqa: PLC0415
        from ..models.api_user_filter_tags_item import ApiUserFilterTagsItem  # noqa: PLC0415

        d = dict(src_dict)
        _application = d.pop("application", UNSET)
        application: ApiIncludeExclude | Unset
        if isinstance(_application, Unset):
            application = UNSET
        else:
            application = ApiIncludeExclude.from_dict(_application)

        _distribution = d.pop("distribution", UNSET)
        distribution: ApiIncludeExclude | Unset
        if isinstance(_distribution, Unset):
            distribution = UNSET
        else:
            distribution = ApiIncludeExclude.from_dict(_distribution)

        _known = d.pop("known", UNSET)
        known: ApiIncludeExclude | Unset
        if isinstance(_known, Unset):
            known = UNSET
        else:
            known = ApiIncludeExclude.from_dict(_known)

        last_seen = d.pop("lastSeen", UNSET)

        _package = d.pop("package", UNSET)
        package: ApiIncludeExclude | Unset
        if isinstance(_package, Unset):
            package = UNSET
        else:
            package = ApiIncludeExclude.from_dict(_package)

        _path = d.pop("path", UNSET)
        path: ApiIncludeExclude | Unset
        if isinstance(_path, Unset):
            path = UNSET
        else:
            path = ApiIncludeExclude.from_dict(_path)

        profiles = cast(list[str], d.pop("profiles", UNSET))

        severities = cast(list[str], d.pop("severities", UNSET))

        show_excluded = d.pop("showExcluded", UNSET)

        sources = cast(list[str], d.pop("sources", UNSET))

        _tags = d.pop("tags", UNSET)
        tags: list[ApiUserFilterTagsItem] | Unset = UNSET
        if _tags is not UNSET:
            tags = []
            for tags_item_data in _tags:
                tags_item = ApiUserFilterTagsItem.from_dict(tags_item_data)

                tags.append(tags_item)

        api_user_filter = cls(
            application=application,
            distribution=distribution,
            known=known,
            last_seen=last_seen,
            package=package,
            path=path,
            profiles=profiles,
            severities=severities,
            show_excluded=show_excluded,
            sources=sources,
            tags=tags,
        )

        api_user_filter.additional_properties = d
        return api_user_filter

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
