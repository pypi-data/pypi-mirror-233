import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.backends.backend import Backend
from komodo_cli.backends.backend_factory import BackendFactory
from komodo_cli.types import (JobNotFoundException,
                              JobNotInDesiredStateException, JobStatus,
                              LocalJobNotFoundException)
from komodo_cli.utils import APIClient, update_context_with_api_client


@click.command("delete")
@click.argument(
    "job_id",
    type=str,
)
@click.option(
    "--force",
    "-f",
    type=bool,
    is_flag=True,
    help="Set this flag if you want to delete the job even if the job is still running",
)
@click.pass_context
def cmd_delete(ctx: click.Context, job_id: str, force: bool):
    """Delete a Komodo job."""
    update_context_with_api_client(ctx)
    logger.info(f"Job ID: {job_id}")

    api_client: APIClient = ctx.obj["api_client"]

    if job_id == "all":
        jobs = api_client.list_jobs()
    else:
        try:
            jobs = [api_client.get_job(job_id)]
        except JobNotFoundException:
            printing.error(f"Job {job_id} does not exist", bold=True)
            return

    for job in jobs:
        backend_schema = api_client.get_backend(job.backend_name)
        backend: Backend = BackendFactory.get_backend(
            backend_schema,
            api_client,
        )

        printing.warning(f"Deleting job {job.id}", bold=True)
        try:
            if not force and job.status not in [
                JobStatus.CANCELLED,
                JobStatus.CANCELLING,
                JobStatus.ERROR,
                JobStatus.UNKNOWN,
                JobStatus.FINISHED,
                JobStatus.NOT_FOUND,
            ]:
                printing.error(
                    f"Job {job.id} has not finished, and --force flag was not set",
                    bold=True,
                )
                return
            backend.delete(job.backend_job_id)
        except JobNotFoundException as e:
            printing.error(f"Job {job.id} does not exist", bold=True)
            return
        except LocalJobNotFoundException:
            if not force:
                printing.info(
                    f"Local job cannot be found on this machine. Use --force to delete anyways."
                )
                return
        except Exception as e:
            printing.error(f"Unexpected exception: {str(e)}", bold=True)
            raise e

        try:
            api_client.delete_job(job.id, force)
        except (JobNotFoundException, JobNotInDesiredStateException) as e:
            if not force:
                printing.error(str(e), bold=True)
                raise e
        except Exception as e:
            printing.error(
                f"Error deleting job {job.id}",
                bold=True,
            )
            raise e
