# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import JSONField
from drf_misc.core.models import AbstractModel

from .constants import TaskStatus


class Task(AbstractModel):
    id = models.CharField(unique=True, primary_key=True, max_length=36)
    name = models.CharField(max_length=200)
    task_name = models.CharField(max_length=200, null=True, blank=True)
    remark = models.TextField(blank=True, null=True)
    identifiers = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default=TaskStatus.RUNNING, choices=TaskStatus.choices)
    response = JSONField(blank=True, null=True)
    counter = models.IntegerField(default=1)
    retries = models.CharField(max_length=20, blank=True, null=True)
    expires = models.CharField(max_length=20, blank=True, null=True)
    root_id = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        db_table = "background_task"
