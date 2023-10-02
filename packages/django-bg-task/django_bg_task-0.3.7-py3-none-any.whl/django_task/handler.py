# -*- coding: utf-8 -*-

import celery
from drf_misc.core.api_exceptions import BadRequest

from .constants import TaskStatus
from .models import Task
from .services import TaskService
from .settings import logger

# pylint: disable=no-member,import-error,too-many-arguments


class TaskHandler(celery.Task):
    def run(self, *args, **kwargs):
        logger.info("Running: %s with args: %s, kwargs: %s", self.name, args, kwargs)

    def before_start(self, task_id, args, kwargs):
        logger.info("Before started: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        if not kwargs.get("identifiers"):
            raise BadRequest({"message": "identifiers is required"})
        identifiers = kwargs.pop("identifiers")
        if not Task.objects.filter(id=task_id).exists():
            data = {
                "identifiers": identifiers,
                "id": task_id,
                "name": self.name,
                "task_name": identifiers.pop(
                    "task_name", getattr(self, "task_name") if hasattr(self, "task_name") else None
                ),
                "remark": identifiers.pop("remark", getattr(self, "remark") if hasattr(self, "remark") else None),
                "status": TaskStatus.RUNNING,
                "retries": self.request.retries,
                "expires": self.request.expires,
                "root_id": self.request.root_id,
            }
            TaskService().create(data=data)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Failure: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        TaskService(task_id).update(
            {
                "status": TaskStatus.ERROR,
                "response": {"message": str(exc)},
            }
        )

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info("On Retry: %s with args: %s, kwargs: %s", task_id, args, kwargs)
        task_instance = Task.objects.filter(id=task_id).first()
        TaskService(task_id).update(
            {
                "status": TaskStatus.RUNNING,
                "counter": task_instance.counter + 1,
            }
        )

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info("After return: %s with args: %s, kwargs: %s, retval: %s", task_id, args, kwargs, retval)
        if retval[0]:
            status = TaskStatus.SUCCESS
        else:
            status = TaskStatus.FAILED
        TaskService(task_id).update(
            {
                "status": status,
                "response": retval[1],
            }
        )
