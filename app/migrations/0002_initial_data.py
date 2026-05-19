from datetime import datetime

from django.db import migrations
from django.utils import timezone


def add_initial_data(apps, schema_editor):
    FuelType = apps.get_model("app", "FuelType")
    FuelItem = apps.get_model("app", "FuelItem")
    IssueRecord = apps.get_model("app", "IssueRecord")

    diesel = FuelType.objects.create(
        name="Diesel",
        description="Дизельне пальне для вантажівок, тракторів та генераторів.",
    )
    gasoline = FuelType.objects.create(
        name="Gasoline A-95",
        description="Бензин для службових автомобілів.",
    )
    oil = FuelType.objects.create(
        name="Engine Oil",
        description="Моторна олива для планового обслуговування техніки.",
    )

    diesel_item = FuelItem.objects.create(
        name="Diesel Euro 5",
        supplier="OKKO Supply",
        quantity_liters=5200,
        unit_price="56.00",
        description="Основний резерв дизельного пального для техніки.",
        fuel_type=diesel,
    )
    gasoline_item = FuelItem.objects.create(
        name="Gasoline A-95 Reserve",
        supplier="WOG Partner",
        quantity_liters=2800,
        unit_price="59.00",
        description="Резерв бензину для службових автомобілів.",
        fuel_type=gasoline,
    )
    oil_item = FuelItem.objects.create(
        name="Oil 10W-40 Fleet",
        supplier="Shell Distributor",
        quantity_liters=650,
        unit_price="185.00",
        description="Олива для технічного обслуговування двигунів.",
        fuel_type=oil,
    )

    IssueRecord.objects.create(
        fuel_item=diesel_item,
        amount_liters=120,
        destination="Трактор МТЗ-82",
        issued_at=timezone.make_aware(datetime(2026, 5, 10, 9, 30)),
    )
    IssueRecord.objects.create(
        fuel_item=gasoline_item,
        amount_liters=40,
        destination="Службовий автомобіль",
        issued_at=timezone.make_aware(datetime(2026, 5, 12, 14, 15)),
    )
    IssueRecord.objects.create(
        fuel_item=oil_item,
        amount_liters=25,
        destination="Планове ТО генератора",
        issued_at=timezone.make_aware(datetime(2026, 5, 15, 11, 0)),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
