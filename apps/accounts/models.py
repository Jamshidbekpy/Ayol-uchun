from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.utils import timezone

class PhoneVerification(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    
class DeleteReason(models.TextChoices):
    I_CHANGED_MY_MIND = "I_CHANGED_MY_MIND", _("I changed my mind")
    THE_INFORMATION_WAS_ENTERED_INCORRECTLY = (
        "THE_INFORMATION_WAS_ENTERED_INCORRECTLY",
        _("The information was entered incorrectly"),
    )
    I_WAS_FORCED = "I_WAS_FORCED", _("I was forced")
    I_PREFER_NOT_TO_SAY = "I_PREFER_NOT_TO_SAY", _("I prefer not to say")
    OTHER = "OTHER", _("Other")


class User(AbstractUser):
    username = None
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    email = models.EmailField(unique=True, verbose_name=_("Email"), blank=True)
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name=_("Phone number")
    )
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is deleted"))
    reason_delete_choices = models.CharField(
        max_length=50,
        choices=DeleteReason.choices,
        blank=True,
        null=True,
        verbose_name=_("Reason for deletion"),
    )
    reason_delete_str = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Other reason (if OTHER selected)"),
    )
    interest = models.ManyToManyField(
        "Interest", blank=True, through="UserInterest", verbose_name=_("Interests")
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD: ClassVar[str] = "phone_number"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["email"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Interest(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    class Meta:
        ordering: ClassVar[list[str]] = ["name"]
        verbose_name = _("Interest")
        verbose_name_plural = _("Interests")

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    interest = models.ForeignKey(
        Interest, on_delete=models.CASCADE, verbose_name=_("Interest")
    )

    class Meta:
        unique_together: list[tuple] = [("user", "interest")]
        verbose_name = _("User Interest")
        verbose_name_plural = _("User Interests")
