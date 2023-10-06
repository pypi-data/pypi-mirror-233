# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from collections import namedtuple

from es7s.shared import FanInfo
from es7s.shared import SocketMessage
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector
from ._state import _BoolState, CheckMenuItemConfig


ValueRange = namedtuple("ValueRange", ["min", "max", "shift"])


class IndicatorFanSpeed(_BaseIndicator[FanInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.fan"

        self._show_rpm = _BoolState(
            config_var=(self.config_section, "label-rpm"),
            gconfig=CheckMenuItemConfig("Show value (RPM)", sep_before=True),
        )

        self._val_range = ValueRange(
            self.uconfig().get("value-min", int, fallback=0),
            self.uconfig().get("value-max", int, fallback=5000),
            self.uconfig().get("value-shift", int, fallback=0),
        )

        super().__init__(
            indicator_name="fan",
            socket_topic="fan",
            icon_selector=ThresholdIconSelector(
                subpath="fan",
                path_dynamic_tpl="%d.png",
                thresholds=[96, 84, 72, 60, 48, 36, 24, 12, 0],
            ),
            title="Fan speed",
            states=[self._show_rpm],
        )

    def _render(self, msg: SocketMessage[FanInfo]):
        value = msg.data.max()
        ratio = 100 * (value + self._val_range.shift - self._val_range.min) / self._val_range.max

        self._update_details("\n".join(f"· {v} RPM" for v in msg.data.values_rpm))
        value_str = str(value or "OFF") if self._show_rpm else ""

        self._render_result(
            value_str,
            value_str,
            False,  # warning,
            self._icon_selector.select(ratio),
        )
