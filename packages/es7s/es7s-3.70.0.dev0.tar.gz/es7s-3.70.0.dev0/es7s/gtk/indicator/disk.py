# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import itertools
from functools import cached_property
from typing import Iterable

from pytermor import format_auto_float

from es7s.shared import DiskUsageInfo, DiskInfo, DiskIoInfo, DiskIoInfoStats
from es7s.shared import SocketMessage
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector, IconEnum
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class DiskIconEnum(IconEnum):
    WAIT = "wait.svg"


class DiskIconPartActivityEnum(IconEnum):
    MIN = "min"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAX = "max"


class DiskIconSelector(ThresholdIconSelector):
    def __init__(self):
        super().__init__(
            subpath="disk",
            path_dynamic_tpl="%s-%d.svg",
            thresholds=[
                100,
                99,
                98,
                95,
                92,
                *range(90, -10, -10),
            ],
            default_value=(DiskIconPartActivityEnum.MIN, 0),
        )

    def select(self, disk_usage: DiskUsageInfo = None, disk_io: DiskIoInfo = None) -> str:
        if override := super(ThresholdIconSelector, self).select():
            return override

        if not disk_usage or not disk_io:
            return DiskIconEnum.WAIT

        io_subtype = self._get_io_subtype((disk_io.read.ratio + disk_io.write.ratio) / 2)
        usage_subtype = self._get_threshold_by_cv(disk_usage.used_perc)
        return self._path_dynamic_tpl % (io_subtype, usage_subtype)

    def _get_io_subtype(self, ratio: float) -> IconEnum:
        if ratio > 0.99:
            return DiskIconPartActivityEnum.MAX
        if ratio > 0.75:
            return DiskIconPartActivityEnum.HIGH
        if ratio > 0.25:
            return DiskIconPartActivityEnum.MEDIUM
        if ratio > 0.05:
            return DiskIconPartActivityEnum.LOW
        return DiskIconPartActivityEnum.MIN

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            yield from DiskIconEnum
            for pts in itertools.product(
                [*DiskIconPartActivityEnum],
                self._thresholds,
            ):
                yield self._compose_path(pts)

        return set(_iter())

    def _compose_path(self, frames: list[str | None]) -> str:
        return self._path_dynamic_tpl % frames


class IndicatorDisk(_BaseIndicator[DiskInfo, DiskIconSelector]):
    def __init__(self):
        self.config_section = "indicator.disk"

        self._show_perc = _BoolState(
            config_var=(self.config_section, "label-used"),
            gconfig=CheckMenuItemConfig("Show used space (%)", sep_before=True),
        )
        self._show_bytes = _BoolState(
            config_var=(self.config_section, "label-free"),
            gconfig=CheckMenuItemConfig("Show free space (GB/TB)"),
        )

        self._show_io_off = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No IO speed", sep_before=True, group=self.config_section),
        )
        self._show_io_read = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="read",
            gconfig=RadioMenuItemConfig("Show read speed (MB/s)", group=self.config_section),
        )
        self._show_io_write = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="write",
            gconfig=RadioMenuItemConfig("Show write speed (MB/s)", group=self.config_section),
        )
        self._show_io_max = _BoolState(
            config_var=(self.config_section, "label-io"),
            config_var_value="max",
            gconfig=RadioMenuItemConfig("Show IO speed (max, MB/s)", group=self.config_section),
        )

        self._used_warn_ratio: float | None = self.uconfig().get(
            "used-warn-level-ratio", float, fallback=None
        )
        self._io_warn_ratio: float | None = self.uconfig().get(
            "io-warn-level-ratio", float, fallback=None
        )

        super().__init__(
            indicator_name="disk",
            socket_topic=["disk-usage", "disk-io"],
            icon_selector=DiskIconSelector(),
            title="Storage",
            states=[
                self._show_perc,
                self._show_bytes,
                self._show_io_off,
                self._show_io_read,
                self._show_io_write,
                self._show_io_max,
            ],
        )

    #
    def _render(self, msg: SocketMessage[DiskInfo]):
        usage_dto = self._get_last_dto(DiskUsageInfo)
        io_dto = self._get_last_dto(DiskIoInfo)

        if isinstance(msg.data, DiskUsageInfo):
            usage_dto = msg.data
        elif isinstance(msg.data, DiskIoInfo):
            io_dto = msg.data

        details = []
        used_ratio = None
        usage_free = None

        if usage_dto:
            used_ratio = usage_dto.used_perc / 100
            usage_free = usage_dto.free
            details.append(
                "Usage\t\t"
                + self._format_used_value(used_ratio)
                + " used / "
                + "".join(self._format_free_value(round(usage_dto.free)))
                + " free"
            )

        io_read_mbps = None
        io_write_mbps = None
        io_ratio = None

        if io_dto:
            io_ratio = (io_dto.read.ratio + io_dto.write.ratio) / 2
            io_read_mbps = io_dto.read.mbps
            io_write_mbps = io_dto.write.mbps
            details.extend(
                [
                    self._format_details_io_value("Read  ↑", io_dto.read),
                    self._format_details_io_value("Write ↓", io_dto.write),
                ]
            )

        self._update_details("\n".join(details))
        self._render_result(
            self._format_result(used_ratio, usage_free, io_read_mbps, io_write_mbps),
            self._format_result(100, 1e10, io_read_mbps, io_write_mbps),
            self._is_warning(used_ratio, io_ratio),  # warning,
            self._icon_selector.select(usage_dto, io_dto),
        )

    def _is_warning(self, used_ratio: float | None, io_ratio: float | None) -> bool:
        used_warn = self._used_warn_ratio and used_ratio and used_ratio >= self._used_warn_ratio
        io_warn = self._io_warn_ratio and io_ratio and io_ratio >= self._io_warn_ratio
        return used_warn or io_warn

    def _format_result(
        self,
        used_ratio: float = None,
        free: float = None,
        read_mbps: float = None,
        write_mbps: float = None,
    ) -> str:
        parts = []
        if used_ratio is not None and self._show_perc:
            parts += [self._format_used_value(used_ratio)]
        if free is not None and self._show_bytes:
            parts += ["".join(self._format_free_value(round(free)))]
        if read_mbps is not None and self._show_io_read:
            parts.append(self._format_io_value("↑", read_mbps))
        elif write_mbps is not None and self._show_io_write:
            parts.append(self._format_io_value("↓", write_mbps))
        elif read_mbps is not None and write_mbps is not None and self._show_io_max:
            parts.append(self._format_io_value("", max(read_mbps, write_mbps)))
        return " ".join(parts).rstrip()

    def _format_used_value(self, used_ratio: float) -> str:
        return f"{100 * used_ratio:3.0f}%"

    def _format_free_value(self, free: int) -> tuple[str, str]:
        free_gb = free / 1000**3
        free_tb = free / 1000**4
        if free_gb < 1:
            return "< 1G", ""
        if free_gb < 1000:
            return format_auto_float(free_gb, 3, False), "G"
        return format_auto_float(free_tb, 3, False), "T"

    def _format_io_value(self, type: str, mbps: float) -> str:
        return f"{type}{mbps:.2f}M"

    def _format_details_io_value(self, type: str, io: DiskIoInfoStats) -> str:
        return f"{type}\t{io.mbps:5.2f} / {io.max_mbps:.0f} Mbps\t({100 * io.ratio:3.2f}%)"
