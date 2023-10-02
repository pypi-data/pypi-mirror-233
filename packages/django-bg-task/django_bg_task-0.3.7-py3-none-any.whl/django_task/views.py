# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from drf_misc.core.api_views import CreateMM, DestroyMM, ListMM, RetrieveMM, UpdateMM
from drf_misc.core.filter_backend import FlexFieldsFilterBackend
from rest_framework import filters

from .models import Task
from .serializers import TaskSerializer
from .services import TaskService


class TaskViewset(CreateMM, ListMM, UpdateMM, DestroyMM, RetrieveMM):
    queryset = Task.objects.filter().order_by("-created_at")
    serializer_class = TaskSerializer
    service_class = TaskService
    model = Task
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        FlexFieldsFilterBackend,
    )

    # Change logic
    filterset_fields = ["status"]
    search_fields = ()

    def get_queryset(self):
        company_id = self.request.auth_user.get("company_id")
        if company_id:
            company_qs = self.queryset.filter(identifiers__company_id=company_id)
            self.queryset = company_qs
        return self.queryset
