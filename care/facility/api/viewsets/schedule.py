from django_filters import rest_framework as filters
from dry_rest_permissions.generics import DRYPermissionFiltersBase, DRYPermissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care.facility.api.serializers.schedule import (
    ScheduleCreateSerializer,
    ScheduleExceptionCreateSerializer,
    ScheduleExceptionReadOnlySerializer,
    ScheduleReadOnlySerializer,
    ScheduleUpdateSerializer,
)
from care.facility.models.schedule import (
    RESOURCE_TO_MODEL,
    Availability,
    Schedule,
    ScheduleException,
    ScheduleResourceType,
)
from care.users.models import User

RESOURCE_FILTER_KEYS = {
    "doctor_id": RESOURCE_TO_MODEL[ScheduleResourceType.DOCTOR],
}


class ScheduleFilterSet(filters.FilterSet):
    date_from = filters.DateFilter(field_name="valid_from", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="valid_to", lookup_expr="lte")


class ScheduleDRYFilterSet(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            pass
        elif request.user.user_type >= User.TYPE_VALUE_MAP["StateLabAdmin"]:
            queryset = queryset.filter(resource__facility__state=request.user.state)
        elif request.user.user_type >= User.TYPE_VALUE_MAP["DistrictLabAdmin"]:
            queryset = queryset.filter(
                resource__facility__district=request.user.district
            )
        else:
            queryset = queryset.filter(
                resource__facility__users__id__exact=request.user.id
            )

        for key, model in RESOURCE_FILTER_KEYS.items():
            value = request.query_params.get(key)
            if value:
                return queryset.filter(
                    resource__resource_id=value,
                    resource__resource_type=model,
                )

        return queryset.none()


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related("resource").all()
    permission_classes = (IsAuthenticated, DRYPermissions)
    filter_backends = [
        ScheduleDRYFilterSet,
        filters.DjangoFilterBackend,
    ]
    filterset_class = ScheduleFilterSet
    lookup_field = "external_id"

    def get_serializer_class(self):
        if self.action in ("create", "delete_availability"):
            return ScheduleCreateSerializer
        if self.action in ("update", "partial_update"):
            return ScheduleUpdateSerializer
        return ScheduleReadOnlySerializer

    @action(
        detail=True,
        methods=["delete"],
        url_path="availability/(?P<availability_external_id>[^/.]+)",
    )
    def delete_availability(self, *args, availability_external_id=None, **kwargs):
        try:
            availability = Availability.objects.get(
                external_id=availability_external_id,
                schedule__external_id=kwargs["external_id"],
            )
            availability.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Availability.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ScheduleExceptionViewSet(viewsets.ModelViewSet):
    queryset = ScheduleException.objects.all()
    permission_classes = (IsAuthenticated, DRYPermissions)
    filter_backends = [
        ScheduleDRYFilterSet,
        filters.DjangoFilterBackend,
    ]
    filterset_class = ScheduleFilterSet
    lookup_field = "external_id"

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ScheduleExceptionCreateSerializer
        return ScheduleExceptionReadOnlySerializer
