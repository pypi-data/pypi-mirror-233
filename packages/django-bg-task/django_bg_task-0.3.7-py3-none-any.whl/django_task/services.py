# -*- coding: utf-8 -*-
import time

from drf_misc.core.services import BaseService

from .models import Task
from .serializers import TaskSerializer


class TaskService(BaseService):
    serializer = TaskSerializer
    model = Task

    def create(self, data, request=None, audit_data=None):
        data["created_at"] = int(time.time())
        return super().create(data, request, audit_data)

    def update(self, data, request=None, audit_data=None, partial=True):
        data["updated_at"] = int(time.time())
        return super().update(data, request, audit_data=audit_data, partial=partial)
