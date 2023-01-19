from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Teaser(models.Model):
    class Category(models.TextChoices):
        FIRST = "C1", _("First category")
        SECOND = "C2", _("Second category")

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        REJECTED = "rejected", _("Rejected")

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    category = models.CharField(
        max_length=10, choices=Category.choices, default=Category.FIRST
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
