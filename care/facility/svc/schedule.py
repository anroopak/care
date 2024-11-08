from datetime import datetime

from django.db.models import QuerySet
from django.utils import timezone

from care.facility.models.schedule import (
    Availability,
    AvailabilityException,
)


def is_available(resource, from_datetime: datetime, to_datetime: datetime) -> bool:
    msg = "Not implemented"
    raise NotImplementedError(msg)


def get_current_schedule(resource) -> QuerySet[Availability]:
    now = timezone.now()
    return Availability.objects.filter(
        schedule__resource=resource,
        schedule__valid_from__lte=now,
        schedule__valid_to__gte=now,
    )


def get_exceptions(resource) -> QuerySet[AvailabilityException]:
    return AvailabilityException.objects.filter(resource=resource)
