from datetime import datetime, time

from freezegun import freeze_time
from pydantic import BaseModel, ValidationError
from requests import Response
from rest_framework import status
from rest_framework.test import APITestCase

from care.facility.models.schedule import (
    Availability,
    SchedulableResource,
    Schedule,
    ScheduleException,
    SlotType,
)
from care.users.models import User
from care.utils.tests.test_utils import TestUtils


@freeze_time("2024-11-01")
class TestScheduleException(TestUtils, APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.state = cls.create_state()
        cls.district = cls.create_district(cls.state)
        cls.local_body = cls.create_local_body(cls.district)

        cls.user = cls.create_user(
            "staff", district=cls.district, local_body=cls.local_body
        )

        cls.facility = cls.create_facility(cls.user, cls.district, cls.local_body)
        cls.doctor_user = cls.create_user(
            "doctor",
            district=cls.district,
            local_body=cls.local_body,
            user_type=User.TYPE_VALUE_MAP["Doctor"],
            home_facility=cls.facility,
        )

        cls.schedulable_resource = SchedulableResource.objects.create(
            facility=cls.facility, resource=cls.doctor_user
        )
        cls.schedule = Schedule.objects.create(
            resource=cls.schedulable_resource,
            valid_from="2024-11-01",
            valid_to="2024-11-30",
        )

        # for monday to friday, availability for appointment 10-12 and open slots 14-16

        Availability.objects.create(
            schedule=cls.schedule,
            slot_type=SlotType.APPOINTMENT,
            slot_size_in_minutes=30,
            tokens_per_slot=10,
            days_of_week=[1, 2, 3, 4, 5],
            start_time=time(hour=10),
            end_time=time(hour=12),
        )
        Availability.objects.create(
            schedule=cls.schedule,
            slot_type=SlotType.OPEN,
            slot_size_in_minutes=0,
            tokens_per_slot=0,
            days_of_week=[1, 2, 3, 4, 5],
            start_time=time(hour=14),
            end_time=time(hour=16),
        )

        # he is on leave from 2024-11-05 to 2024-11-07
        ScheduleException.objects.create(
            resource=cls.schedulable_resource,
            is_available=False,
            slot_size_in_minutes=0,
            tokens_per_slot=0,
            datetime_range=(datetime(2024, 11, 5), datetime(2024, 11, 7)),
        )

        # he compensates for appointment on 2024-11-09 Saturday from 10-12
        ScheduleException.objects.create(
            resource=cls.schedulable_resource,
            is_available=True,
            slot_size_in_minutes=0,
            tokens_per_slot=0,
            datetime_range=(
                datetime(2024, 11, 9, hour=10),
                datetime(2024, 11, 9, hour=12),
            ),
        )

    def get_url(self, entry_id=None, action=None):
        base_url = f"/api/v1/facility/{self.facility.external_id}/schedule_exceptions/"
        if entry_id is not None:
            base_url += f"{entry_id}/"
        if action is not None:
            base_url += f"{action}/"
        return base_url

    def get_response_schema(self):
        class ScheduleExceptionResponseSchema(BaseModel):
            id: str
            name: str
            is_available: bool
            datetime_range: list[datetime]
            slot_type: SlotType
            slot_size_in_minutes: int
            tokens_per_slot: int

        return ScheduleExceptionResponseSchema

    def assert_response_schema(self, response: Response, schema: BaseModel):
        try:
            schema.validate(response.json())
        except ValidationError as e:
            raise e

    def test_create_schedule(self):
        # test create schedule for doctor user in december month
        data = {
            "name": "test schedule",
            "doctor_username": self.doctor_user.username,
            "is_available": True,
            "datetime_range": [
                "2024-12-09T10:00:00",
                "2024-12-09T12:00:00",
            ],
            "slot_type": SlotType.APPOINTMENT,
            "slot_size_in_minutes": 30,
            "tokens_per_slot": 10,
        }
        response = self.client.post(self.get_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if the response is as per the spec
        response_json_schema = self.get_response_schema()
        self.assert_response_schema(response, response_json_schema)

    def test_update_schedule_exception(self):
        schedule_exception = ScheduleException.objects.create(
            resource=self.schedulable_resource,
            name="test schedule exception",
            is_available=True,
            datetime_range=(
                datetime(2024, 12, 9, hour=10),
                datetime(2024, 12, 9, hour=12),
            ),
            slot_size_in_minutes=30,
            tokens_per_slot=10,
            slot_type=SlotType.APPOINTMENT,
        )
        data = {
            "name": "test schedule exception 2",
            "slot_size_in_minutes": 45,
        }
        url = self.get_url(schedule_exception.external_id)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if the response is as per the spec
        response_json_schema = self.get_response_schema()
        self.assert_response_schema(response, response_json_schema)

        # check if the availability is updated
        schedule_exception.refresh_from_db()
        self.assertEqual(schedule_exception.slot_size_in_minutes, 45)
