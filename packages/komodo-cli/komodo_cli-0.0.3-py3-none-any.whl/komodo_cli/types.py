from enum import Enum
from typing import List, Optional


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    ERROR = "error"
    UNKNOWN = "unknown"
    NOT_FOUND = "not found"
    UNAUTHORIZED = "unauthorized"
    UNREACHABLE = "unreachable"


LOCAL_STATUS_MAPPING = {
    "cancelling": JobStatus.CANCELLING,
    "cancelled": JobStatus.CANCELLED,
    "created": JobStatus.PENDING,
    "running": JobStatus.RUNNING,
    "paused": JobStatus.RUNNING,
    "restarting": JobStatus.PENDING,
    "removing": JobStatus.FINISHED,
    "exited": JobStatus.FINISHED,
    "dead": JobStatus.FINISHED,
}


class JobNotFoundException(Exception):
    pass


class LocalJobNotFoundException(Exception):
    pass


class JobNotInDesiredStateException(Exception):
    pass


class Job:
    def __init__(
        self,
        backend_name: str,
        resource_name: Optional[str],
        id: str,
        backend_job_id: Optional[str],
        command: str,
        image: str,
        status: JobStatus,
    ):
        self.backend_name = backend_name
        self.resource_name = resource_name
        self.id = id
        self.backend_job_id = backend_job_id
        self.command = command
        self.image = image
        self.status = status

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        obj.status = JobStatus(d["status"])
        return obj

    def to_dict(self):
        return {
            "backend_name": self.backend_name,
            "resource_name": self.resource_name,
            "id": self.id,
            "backend_job_id": self.backend_job_id,
            "command": self.command,
            "image": self.image,
            "status": self.status.name,
        }


class Machine:
    def __init__(
        self,
        name: str,
        backend_name: str,
        resource_name: Optional[str],
        image: str,
        status: JobStatus,
        backend_job_id: str,
        machine_id: str,
    ):
        self.name = name
        self.backend_name = backend_name
        self.resource_name = resource_name
        self.image = image
        self.status = status
        self.backend_job_id = backend_job_id
        self.machine_id = machine_id

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        obj.status = JobStatus(d["status"])
        return obj

    def to_dict(self):
        return {
            "name": self.name,
            "backend_name": self.backend_name,
            "resource_name": self.resource_name,
            "backend_job_id": self.backend_job_id,
            "image": self.image,
            "status": self.status.name,
            "machine_id": self.machine_id,
        }


class Resource:
    def __init__(
        self,
        name: str,
        config: dict,
    ):
        self.name = name
        self.config = config

    @classmethod
    def from_dict(cls, d):
        obj = cls(**d)
        return obj

    def to_dict(self):
        d = {
            "name": self.name,
            "config": self.config,
        }
        return d


class Backend:
    def __init__(
        self,
        name: str,
        type: str,
        config: dict,
        resources: List[Resource],
    ):
        self.name = name
        self.type = type
        self.config = config
        self.resources = resources

    @classmethod
    def from_dict(cls, d):
        resources_dicts = d["resources"]
        resources = [Resource.from_dict(r) for r in resources_dicts]
        obj = cls(
            name=d["name"],
            type=d["type"],
            config=d["config"],
            resources=resources,
        )
        return obj

    def to_dict(self):
        d = {
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "resources": [r.to_dict() for r in self.resources],
        }
        return d
