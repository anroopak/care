from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models

from care.facility.models.base import FacilityBaseModel
from care.facility.models.mixins.permissions.facility import (
    FacilityRelatedPermissionMixin,
)


class Schedule(FacilityBaseModel, FacilityRelatedPermissionMixin):
    resource = GenericForeignKey(
        "resource_type",
        "resource_id",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    valid_from = models.DateTimeField(null=False, blank=False)
    valid_to = models.DateTimeField(null=False, blank=False)


class Availability(FacilityBaseModel, FacilityRelatedPermissionMixin):
    schedule = models.ForeignKey(
        "Schedule", on_delete=models.CASCADE, null=False, blank=False
    )
    type = models.CharField(max_length=255, null=False, blank=False)
    slot_size_in_minutes = models.IntegerField(null=False, blank=False)
    tokens_per_slot = models.IntegerField(null=False, blank=False)
    day_of_week = models.IntegerField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)


class AvailabilityException(FacilityBaseModel, FacilityRelatedPermissionMixin):
    type = models.CharField(max_length=255, null=False, blank=False)
    is_available = models.BooleanField(null=False, blank=False)
    datetime_range = DateTimeRangeField(null=False, blank=False)
