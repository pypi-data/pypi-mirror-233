from typing import Any
from typing import Dict
from typing import Tuple


def execute_dbt_patching() -> None:
    patch_dbt_collect_parts()


# IF you run sqlfluff + dbt compiler without using a CLI, some of the logic is not prepared for it
# so we have a patch function that fixes up the logic to not break.
def patch_dbt_collect_parts() -> None:
    @classmethod  # type: ignore
    def collect_parts(cls: Any, args: Any) -> Tuple[Any, Any]:
        from dbt.config import Project
        from dbt.config.renderer import DbtProjectYamlRenderer

        if isinstance(getattr(args, "vars", "{}"), dict):
            setattr(args, "vars", "{}")

        from dbt.config.utils import parse_cli_vars

        cli_vars: Dict[str, Any] = parse_cli_vars(getattr(args, "vars", "{}"))
        profile = cls.collect_profile(args=args)
        project_renderer = DbtProjectYamlRenderer(profile, cli_vars)
        project = cls.collect_project(args=args, project_renderer=project_renderer)
        assert type(project) is Project
        return (project, profile)

    from dbt.config import RuntimeConfig

    RuntimeConfig.collect_parts = collect_parts  # type: ignore
