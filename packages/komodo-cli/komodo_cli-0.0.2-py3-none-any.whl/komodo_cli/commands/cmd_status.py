import click
from loguru import logger
from tabulate import tabulate

import komodo_cli.printing as printing
from komodo_cli.utils import APIClient, update_context_with_api_client


@click.command("status")
@click.argument(
    "job_id",
    type=str,
)
@click.pass_context
def cmd_status(ctx: click.Context, job_id: str):
    """Get status of a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Job ID: {job_id}")

    api_client: APIClient = ctx.obj["api_client"]

    try:
        job = api_client.get_job(job_id)
        jobs_to_print = [
            [
                job.id,
                job.command,
                job.status.value,
                job.backend_name,
                job.resource_name,
                job.backend_job_id,
            ]
        ]

        click.echo(
            tabulate(
                jobs_to_print,
                headers=[
                    "Job ID",
                    "Command",
                    "Status",
                    "Backend",
                    "Resource",
                    "Backend Job ID",
                ],
                tablefmt="simple_grid",
            ),
        )
    except Exception as e:
        printing.error(f"Error getting job {job_id}", bold=True)
        raise e
