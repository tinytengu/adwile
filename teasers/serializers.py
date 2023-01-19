from rest_framework import serializers

from .models import Teaser


class TeaserCreateSerializer(serializers.ModelSerializer):
    """For `create` action only. Excludes `status` and `author` fields from assigning."""

    class Meta:
        model = Teaser
        exclude = ["status", "author"]


class TeaserViewSerializer(serializers.ModelSerializer):
    """For `list` and `detail` actions only. Serializes all model fields."""

    class Meta:
        model = Teaser
        fields = "__all__"


class TeaserUpdateSerializer(serializers.ModelSerializer):
    """For `update` and `partial_udpate` actions only. Prevents `status` and `author` fields from being modified by a regular user."""

    class Meta:
        model = Teaser
        exclude = ["status", "author"]


class TeaserUpdateAdminSerializer(serializers.ModelSerializer):
    """For `update` and `partial_udpate` actions only. Allows to modify any fields for staff members.

    `status` field cannot be changed after setting to anything other than `pending`"""

    def validate_status(self, value: str):
        if self.instance.status != Teaser.Status.PENDING:
            raise serializers.ValidationError(
                f"Unable to change this field from {self.instance.status}"
            )
        return value

    class Meta:
        model = Teaser
        fields = "__all__"
