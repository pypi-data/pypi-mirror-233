import click
from tabulate import tabulate

import komodo_cli.printing as printing
from komodo_cli.utils import APIClient, update_context_with_api_client


@click.command("list")
@click.option("--skip", "-s", type=int, default=0)
@click.option("--limit", "-l", type=int, default=10)
@click.pass_context
def cmd_list(ctx: click.Context, skip: int, limit: int):
    """List Komodo jobs."""
    update_context_with_api_client(ctx)
    api_client: APIClient = ctx.obj["api_client"]

    try:
        jobs = api_client.list_jobs(skip, limit)

        jobs_to_print = [
            [
                job.id,
                job.command,
                job.status.value,
                job.backend_name,
            ]
            for job in jobs
        ]

        printing.header(f"Found {len(jobs)} Komodo jobs\n", bold=True)
        printing.info(
            tabulate(
                jobs_to_print,
                headers=[
                    "Job ID",
                    "Command",
                    "Status",
                    "Backend",
                ],
                tablefmt="simple_grid",
            ),
        )
    except Exception as e:
        printing.error(f"Error listing jobs", bold=True)
        raise e
