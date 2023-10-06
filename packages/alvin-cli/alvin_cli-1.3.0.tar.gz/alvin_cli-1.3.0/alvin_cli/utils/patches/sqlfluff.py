from typing import Any

from alvin_cli.config import settings


def execute_sqlfluff_patching(fluff_config: Any) -> None:
    if settings.alvin_verbose_log:
        patch_logs(fluff_config)


# This enables some useful log statements for troubleshooting, so we can debug
# scenarios were we did not compile the DBT model raw query successfully.
def patch_logs(fluff_config: Any) -> None:
    from sqlfluff.cli.commands import get_linter_and_formatter
    from sqlfluff.cli.commands import set_logging_level
    from sqlfluff.cli.outputstream import make_output_stream

    output_stream = make_output_stream(fluff_config, None, None)
    lnt, formatter = get_linter_and_formatter(fluff_config, output_stream)
    set_logging_level(4, formatter)
