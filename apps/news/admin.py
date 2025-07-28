from django.contrib import admin

from .models import Afisha, Category, CommentVebinar, News, UserVebinar, Vebinar


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "view_count")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    readonly_fields = ("view_count",)
    ordering = ("-created_at",)


@admin.register(Afisha)
class AfishaAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "day", "view_count")
    search_fields = ("title", "description", "location")
    list_filter = ("day",)
    ordering = ("-day",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    search_fields = ("category",)
    ordering = ("category",)


class CommentVebinarInline(admin.TabularInline):
    model = CommentVebinar
    extra = 0
    readonly_fields = ("user", "comment", "grade", "created_at")
    can_delete = False


@admin.register(Vebinar)
class VebinarAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author_fullname",
        "category",
        "day",
        "datetime",
        "grade",
        "is_upcoming",
    )
    search_fields = ("name", "author_fullname", "description")
    list_filter = ("category", "day")
    inlines = [CommentVebinarInline]
    readonly_fields = ("grade", "created_at", "updated_at")
    ordering = ("-datetime",)


@admin.register(CommentVebinar)
class CommentVebinarAdmin(admin.ModelAdmin):
    list_display = ("user", "vebinar", "grade", "created_at")
    search_fields = ("user__email", "vebinar__name", "comment")
    list_filter = ("created_at", "grade")
    ordering = ("-created_at",)


@admin.register(UserVebinar)
class UserVebinarAdmin(admin.ModelAdmin):
    list_display = ("user", "vebinar", "is_sold", "created_at")
    list_filter = ("is_sold", "created_at")
    search_fields = ("user__email", "vebinar__name")
    ordering = ("-created_at",)
