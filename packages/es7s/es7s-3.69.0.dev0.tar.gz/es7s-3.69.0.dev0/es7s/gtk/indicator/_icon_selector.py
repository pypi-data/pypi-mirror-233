# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import abc
import importlib.resources
import typing as t
import pytermor as pt
from abc import abstractmethod
from collections.abc import Iterable
from functools import cached_property, lru_cache
from importlib.abc import Traversable
from pathlib import Path

from es7s import APP_VERSION
from es7s.shared import RESOURCE_PACKAGE, get_logger

IST = t.TypeVar("IST", bound='IIconSelector')


class IconEnum(str, pt.ExtendedEnum):
    def __str__(self) -> str:
        return self.value


class IIconSelector(metaclass=abc.ABCMeta):
    def __init__(self, name_default: str | IconEnum = "apport-symbolic", subpath: str = 'common'):
        self._name_default = name_default
        self._subpath = subpath
        self._demo_state = False
        self._demo_icon_idx = 0

    def select(self, *args) -> str | IconEnum | None:
        if self._demo_state:
            return self._select_demo_next()
        return None

    @property
    @abstractmethod
    def icon_names_set(self) -> set[str | IconEnum]:
        ...

    @property
    def name_default(self) -> str:
        return str(self._name_default)

    @property
    def subpath(self) -> str:
        return self._subpath

    @cached_property
    def theme_path(self) -> Traversable:
        icons_dir = Path(f"icons@{APP_VERSION}")
        if self._subpath:
            icons_dir /= self._subpath
        theme_path = importlib.resources.files(RESOURCE_PACKAGE).joinpath(icons_dir)
        get_logger().debug(f"Theme resource path: '{theme_path}'")
        return theme_path

    @lru_cache
    def get_icon_path(self, name: str | IconEnum = None) -> str:
        path = str(self.theme_path / (name or self.name_default))
        get_logger().debug(f"Resolving icon path: {path!r}")
        return path

    @cached_property
    def icon_names_sorted(self) -> list[str | IconEnum]:
        return sorted(self.icon_names_set)

    def get_icon_demo_state(self) -> bool:
        return self._demo_state

    def set_icon_demo_state(self, enabled: bool):
        self._demo_state = (enabled and len(self.icon_names_set) > 0)

    def _select_demo_next(self) -> str | IconEnum:
        self._demo_icon_idx += 1
        if self._demo_icon_idx >= len(self.icon_names_sorted):
            self._demo_icon_idx = 0
        return self.icon_names_sorted[self._demo_icon_idx]


class StaticIconEnum(IconEnum):
    WARNING = 'warning.svg'


class StaticIconSelector(IIconSelector):
    def select(self, *args) -> str:
        if override := super().select():
            return override
        return self.name_default

    @cached_property
    def icon_names_set(self) -> set[str]:
        return {self.name_default}


class ThresholdIconSelector(IIconSelector):
    def __init__(self, subpath: str, path_dynamic_tpl: str, thresholds: list[int], default_value=0):
        super().__init__(path_dynamic_tpl % default_value, subpath)
        self._path_dynamic_tpl = path_dynamic_tpl
        self._thresholds = thresholds

    def select(self, carrier_value: float) -> str:
        if override := super().select():
            return override
        if not self._thresholds or not self._path_dynamic_tpl:
            return self.name_default

        icon_subtype = self._thresholds[-1]
        for thr in self._thresholds:
            icon_subtype = thr
            if carrier_value >= thr:
                break
        return self._path_dynamic_tpl % icon_subtype

    def _get_threshold_by_cv(self, carrier_value: float) -> int:
        for thr in self._thresholds:
            if carrier_value >= thr:
                return thr
        return self._thresholds[-1]

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            for thr in self._thresholds:
                yield self.select(thr)
        return set(_iter())
