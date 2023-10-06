import logging
from typing import List

import typer
from alvin_api_client.model.impact_analysis_node_list_response import (
    ImpactAnalysisNodeListResponse,
)
from alvin_api_client.model.impact_analysis_platform_request import (
    ImpactAnalysisPlatformRequest,
)
from alvin_api_client.model.impact_analysis_query_request import (
    ImpactAnalysisQueryRequest,
)
from alvin_api_client.model.impact_analysis_request import ImpactAnalysisRequest

from alvin_cli.schemas.models import OutputFormat
from alvin_cli.utils.api_client import default_api
from alvin_cli.utils.check_sql_impact_analysis import run_check_sql_impact_analysis
from alvin_cli.utils.common_arguments import FILE_NAME
from alvin_cli.utils.common_arguments import OUTPUT
from alvin_cli.utils.common_arguments import PLATFORM_ID
from alvin_cli.utils.common_arguments import SAVE_TO_FILE
from alvin_cli.utils.helper_functions import extract_dict
from alvin_cli.utils.helper_functions import handle_print_exception
from alvin_cli.utils.helper_functions import print_node_stats_impact_analysis
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import structure_impact_analysis_data
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


@app.command("check-sql-files")
def check_sql_files_from_dbt(
    sql_models: List[str] = typer.Argument(
        ...,
        help=typer.style(
            "List of SQL files from dbt model separated by space",
            fg=typer.colors.BRIGHT_GREEN,
            bold=True,
        ),
    ),
) -> None:
    """Check SQL Impact Analysis"""
    run_check_sql_impact_analysis(list(sql_models), "target/manifest.json")


@app.command()
def raw_query(
    query_str: str = typer.Option(
        ...,
        "--query_str",
        "-q",
        help=typer.style(
            "SQL query",
            fg=typer.colors.BRIGHT_GREEN,
            bold=True,
        ),
    ),
    platform_id: str = PLATFORM_ID,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Check Impact Analysis From Raw Query Entity"""

    title = "Summary of Impacted Entities"
    if file_name == "":
        file_name = "impact_analysis"

    try:
        request_in_query_validate = ImpactAnalysisRequest(
            query=ImpactAnalysisQueryRequest(source_text=query_str),
            platform=ImpactAnalysisPlatformRequest(id=platform_id),
        )

        query_validation_response = default_api.validate_impact_analysis_query_api_v2_impact_analysis_validate_query_post(
            request_in_query_validate
        )

        if query_validation_response.is_valid_query:

            impact_analysis_response: ImpactAnalysisNodeListResponse = default_api.run_impact_node_query_api_v2_impact_analysis_query_string_nodes_post(
                request_in_query_validate
            )

            print_node_stats_impact_analysis(impact_analysis_response)

            if save_to_file:
                structured_data = structure_impact_analysis_data(
                    impact_analysis_data=impact_analysis_response,
                )

                print_output_format(
                    data=structured_data,
                    table_title=title,
                    output=output,
                    file_name=file_name,
                    save_to_file=save_to_file,
                )

        else:
            typer_secho_raise("Invalid query!", "RED")
            return

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return
