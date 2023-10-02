# -*- coding: utf-8 -*-
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

from .views import TaskViewset

router = SimpleRouter()

router.register("tasks", TaskViewset, basename="tasks")

urlpatterns = router.urls
