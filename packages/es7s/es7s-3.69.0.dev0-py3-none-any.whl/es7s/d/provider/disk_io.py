# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime
import sys
import time, psutil
from copy import copy
import pytermor as pt
from psutil._common import sdiskio

from ._base import DataProvider
from es7s.shared import DiskIoInfo, get_logger, DiskIoInfoStats


class DiskIoProvider(DataProvider[DiskIoInfo]):
    def __init__(self):
        self._prev_ts: int = time.time_ns()
        self._prev_counters: sdiskio | None = None

        self._read_max_mbps = 0.0
        self._write_max_mbps = 0.0
        super().__init__("disk-io", "disk-io", poll_interval_sec=1.0)

    def _collect(self) -> DiskIoInfo:
        counters = psutil.disk_io_counters()
        now_ts = time.time_ns()

        result = self._collect_internal(counters, now_ts)

        self._prev_ts = now_ts
        self._prev_counters = counters
        return result

    def _collect_internal(self, counters: sdiskio, now_ts: int) -> DiskIoInfo:
        delta_t = 1e-9 * (now_ts - self._prev_ts)  # ns -> sec
        if not delta_t or not self._prev_counters:
            return DiskIoInfo()

        # bytes -> megabytes
        mbps_read = 1e-6 * (counters.read_bytes - self._prev_counters.read_bytes) / delta_t
        mbps_write = 1e-6 * (counters.write_bytes - self._prev_counters.write_bytes) / delta_t

        self._read_max_mbps = max(self._read_max_mbps, mbps_read)
        self._write_max_mbps = max(self._write_max_mbps, mbps_write)
        return DiskIoInfo(
            DiskIoInfoStats(mbps_read, self._read_max_mbps),
            DiskIoInfoStats(mbps_write, self._write_max_mbps),
        )

    # def _debug_state(self, dto: DiskIoInfo, now_ts: int):
    #     def _print(*args, sep="|", end='\n', dots=True):
    #         fmt = f"[%-10s] %4s {sep}%10s{sep}%10s{sep}"
    #         get_logger().debug(
    #             f"DISK ACTIVITY " + fmt % args + ["", "." * (now_ts % 3)][dots] + end
    #         )
    #
    #     fsb = pt.format_si_binary
    #     ratio = (dto.read.ratio + dto.write.ratio)/2
    #     if ratio > 0:
    #         pbar = int(ratio / 10) * "#"
    #         perc = f"{ratio:>3.0f}%"
    #         _print(
    #             pbar,perc,
    #             fsb(dto.read.bps) + " R",
    #             fsb(dto.write.bps) + " W",
    #             dots=False,
    #             )
    #     # else:
    #     #     _print("", "--", "", "", end="")
