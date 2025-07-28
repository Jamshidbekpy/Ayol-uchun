from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class News(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    card = models.ImageField(upload_to="news_cards/", verbose_name=_("Image"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View count"))

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News list")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Afisha(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    card = models.ImageField(upload_to="afisha_cards/", verbose_name=_("Image"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    day = models.DateField(verbose_name=_("Event date"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("View count"))

    class Meta:
        verbose_name = _("Afisha")
        verbose_name_plural = _("Afisha list")
        ordering = ["-day"]

    def __str__(self):
        return self.title


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True, verbose_name=_("Category"))

    class Meta:
        verbose_name = _("Webinar Category")
        verbose_name_plural = _("Webinar Categories")
        ordering = ["category"]

    def __str__(self):
        return self.category


class Vebinar(BaseModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    name = models.CharField(max_length=255, verbose_name=_("Webinar name"))
    author_fullname = models.CharField(
        max_length=255, verbose_name=_("Author full name")
    )
    description = models.TextField(verbose_name=_("Description"))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Category")
    )
    day = models.DateField(verbose_name=_("Day"))
    datetime = models.DateTimeField(verbose_name=_("Time"))

    class Meta:
        verbose_name = _("Webinar")
        verbose_name_plural = _("Webinars")
        ordering = ["-datetime"]

    def __str__(self):
        return f"{self.name} ({self.day})"

    @property
    def grade(self):
        comments = self.comments.all()
        if not comments.exists():
            return 0
        return round(sum(c.grade for c in comments) / comments.count(), 2)

    @property
    def is_upcoming(self):
        return self.datetime > timezone.now()


class CommentVebinar(models.Model):
    comment = models.TextField(verbose_name=_("Comment"))
    grade = models.PositiveSmallIntegerField(verbose_name=_("Grade"))
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    vebinar = models.ForeignKey(
        Vebinar,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Webinar"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Webinar Comment")
        verbose_name_plural = _("Webinar Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.vebinar}"


class UserVebinar(BaseModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    vebinar = models.ForeignKey(
        Vebinar, on_delete=models.CASCADE, verbose_name=_("Webinar")
    )
    is_sold = models.BooleanField(default=False, verbose_name=_("Purchased"))

    class Meta:
        verbose_name = _("User Webinar")
        verbose_name_plural = _("User Webinars")
        ordering = ["-created_at"]
        unique_together = ("user", "vebinar")

    def __str__(self):
        return f"{self.user} - {self.vebinar}"
