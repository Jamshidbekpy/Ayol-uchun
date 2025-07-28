from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Status(models.TextChoices):
    USED = "USED", _("Used")
    EXPIRED = "EXPIRED", _("Expired")
    ACTIVE = "ACTIVE", _("Active")


class Category(models.Model):
    category = models.CharField(max_length=255, verbose_name=_("Category name"))
    icon = models.ImageField(upload_to="category_icons/", verbose_name=_("Icon"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category


class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_("Full name"))
    avatar = models.ImageField(upload_to="authors/", verbose_name=_("Avatar"))

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.full_name


class Course(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.PositiveIntegerField(verbose_name=_("Price"))
    card = models.ImageField(upload_to="course_cards/", verbose_name=_("Course image"))
    discount = models.PositiveIntegerField(default=0, verbose_name=_("Discount (%)"))
    discount_time = models.DateTimeField(
        verbose_name=_("Discount expires at"), default=timezone.now
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Category")
    )
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name=_("Author")
    )
    users = models.ManyToManyField(
        "accounts.User", through="UserCourse", verbose_name=_("Users")
    )

    @property
    def grade(self):
        comments = self.comments.all()
        if not comments.exists():
            return 0
        return round(sum(comment.grade for comment in comments) / comments.count(), 2)

    @property
    def is_discount_active(self):
        return self.discount > 0 and self.discount_time > timezone.now()

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title


class Promokod(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    promokod = models.CharField(
        max_length=50, unique=True, verbose_name=_("Promo code")
    )
    discount = models.PositiveIntegerField(default=0, verbose_name=_("Discount (%)"))
    expire_at = models.DateTimeField(verbose_name=_("Expires at"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Promo code")
        verbose_name_plural = _("Promo codes")


class Video(BaseModel):
    video = models.FileField(upload_to="course_videos/", verbose_name=_("Video file"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course")
    )

    class Meta:
        verbose_name = _("Course video")
        verbose_name_plural = _("Course videos")


class CommentCourse(models.Model):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        related_name="comments",
    )
    comment = models.TextField(verbose_name=_("Comment"))
    grade = models.PositiveSmallIntegerField(verbose_name=_("Grade"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Course comment")
        verbose_name_plural = _("Course comments")


class UserCourse(BaseModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name=_("User")
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    is_sold = models.BooleanField(default=False, verbose_name=_("Purchased"))

    class Meta:
        verbose_name = _("User's course")
        verbose_name_plural = _("Users' courses")
