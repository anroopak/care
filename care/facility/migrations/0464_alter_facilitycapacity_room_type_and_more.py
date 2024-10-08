# Generated by Django 4.2.2 on 2024-09-02 09:42

from django.db import migrations, models

from care.facility.models import RoomType


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0463_patientnotes_reply_to"),
    ]

    def migrate_room_type(apps, schema_editor):
        FacilityCapacity = apps.get_model("facility", "FacilityCapacity")

        room_type_migration_map = {
            1: RoomType.GENERAL_BED,  # General Bed
            10: RoomType.ICU_BED,  # ICU
            20: RoomType.ICU_BED,  # Ventilator
            30: RoomType.GENERAL_BED,  # Covid Beds
            100: RoomType.ICU_BED,  # Covid Ventilators
            110: RoomType.ICU_BED,  # Covid ICU
            120: RoomType.OXYGEN_BED,  # Covid Oxygen beds
            150: RoomType.OXYGEN_BED,  # Oxygen beds
            0: RoomType.OTHER,  # Total
            2: RoomType.OTHER,  # Hostel
            3: RoomType.ISOLATION_BED,  # Single Room with Attached Bathroom
            40: RoomType.GENERAL_BED,  # KASP Beds
            50: RoomType.ICU_BED,  # KASP ICU beds
            60: RoomType.OXYGEN_BED,  # KASP Oxygen beds
            70: RoomType.ICU_BED,  # KASP Ventilator beds
        }

        merged_facility_capacities = {}

        for old_type, new_type in room_type_migration_map.items():
            facility_capacities = FacilityCapacity.objects.filter(room_type=old_type)

            for facility_capacity in facility_capacities:
                key = (facility_capacity.facility.external_id, new_type)

                if key not in merged_facility_capacities:
                    merged_facility_capacities[key] = {
                        "facility": facility_capacity.facility,
                        "room_type": new_type,
                        "total_capacity": facility_capacity.total_capacity,
                        "current_capacity": facility_capacity.current_capacity,
                    }
                else:
                    merged_facility_capacities[key]["total_capacity"] += (
                        facility_capacity.total_capacity
                    )
                    merged_facility_capacities[key]["current_capacity"] += (
                        facility_capacity.current_capacity
                    )

                facility_capacity.delete()

        for data in merged_facility_capacities.values():
            FacilityCapacity.objects.create(**data)

    operations = [
        migrations.RunPython(migrate_room_type, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="facilitycapacity",
            name="room_type",
            field=models.IntegerField(
                choices=[
                    (100, "ICU Bed"),
                    (200, "Ordinary Bed"),
                    (300, "Oxygen Bed"),
                    (400, "Isolation Bed"),
                    (500, "Others"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="historicalfacilitycapacity",
            name="room_type",
            field=models.IntegerField(
                choices=[
                    (100, "ICU Bed"),
                    (200, "Ordinary Bed"),
                    (300, "Oxygen Bed"),
                    (400, "Isolation Bed"),
                    (500, "Others"),
                ]
            ),
        ),
    ]
