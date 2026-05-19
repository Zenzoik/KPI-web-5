import hashlib

from django.db import migrations


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def add_demo_users(apps, schema_editor):
    User = apps.get_model("app", "User")
    IssueRecord = apps.get_model("app", "IssueRecord")

    User.objects.create(
        username="admin",
        full_name="Адміністратор",
        hashed_password=hash_password("admin123"),
        role="admin",
    )
    operator = User.objects.create(
        username="operator",
        full_name="Оператор",
        hashed_password=hash_password("user123"),
        role="user",
    )

    IssueRecord.objects.filter(user__isnull=True).update(user=operator)


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_user_issuerecord_user"),
    ]

    operations = [
        migrations.RunPython(add_demo_users),
    ]
