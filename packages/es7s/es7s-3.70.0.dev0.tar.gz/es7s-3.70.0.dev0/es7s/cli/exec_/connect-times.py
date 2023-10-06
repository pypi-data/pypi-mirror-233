# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11
from es7s.cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    short_help="measure connection timings (lookups, redirects)",
)
@cli_argument(
    "url",
    type=str,
    required=True,
    default="localhost",
    nargs=-1,
)
@catch_and_log_and_exit
class invoker:
    """
    @TODO

    Requires ++curl++.
    """
    def __init__(self, **kwargs):
        pass

    def run(self):
        pass
