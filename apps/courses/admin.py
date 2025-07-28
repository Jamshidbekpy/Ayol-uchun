from django.contrib import admin

from .models import Author, Category, CommentCourse, Course, Promokod, UserCourse, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
    )
    search_fields = ("category",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
    )
    search_fields = ("full_name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "discount",
        "discount_time",
        "is_discount_active",
        "category",
        "author",
    )
    list_filter = ("category", "author", "discount_time")
    search_fields = ("title", "description")
    readonly_fields = ("is_discount_active", "grade")
    autocomplete_fields = ["category", "author"]


@admin.register(Promokod)
class PromokodAdmin(admin.ModelAdmin):
    list_display = ("id", "promokod", "course", "discount", "expire_at", "status")
    list_filter = ("status",)
    search_fields = ("promokod",)
    autocomplete_fields = ["course"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "video", "created_at", "updated_at")
    autocomplete_fields = ["course"]


@admin.register(CommentCourse)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "grade", "created_at")
    list_filter = ("grade", "created_at")
    search_fields = ("comment",)
    autocomplete_fields = ["user", "course"]


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "is_sold", "created_at")
    list_filter = ("is_sold",)
    autocomplete_fields = ["user", "course"]
