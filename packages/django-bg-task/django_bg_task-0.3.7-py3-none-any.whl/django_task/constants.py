# -*- coding: utf-8 -*-

# pylint: disable=too-few-public-methods


class TaskStatus:
    SUCCESS = "success"
    RUNNING = "running"
    FAILED = "failed"
    ERROR = "error"

    choices = (
        (RUNNING, "Running"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (ERROR, "Error"),
    )
