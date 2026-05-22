from django.contrib import admin

from .models import Artwork, Category, Comment, Like, Profile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'text', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'description', 'author__username')
    autocomplete_fields = ('author', 'category')
    readonly_fields = ('created_at',)
    inlines = [CommentInline]
    date_hierarchy = 'created_at'

    @admin.display(description='Лайки')
    def likes_count(self, obj):
        return obj.likes.count()

    @admin.display(description='Комментарии')
    def comments_count(self, obj):
        return obj.comments.count()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'location')
    search_fields = ('user__username', 'display_name', 'location')
    autocomplete_fields = ('user',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'artwork', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'artwork__title')
    autocomplete_fields = ('user', 'artwork')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'user', 'short_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'artwork__title')
    autocomplete_fields = ('user', 'artwork')
    readonly_fields = ('created_at',)

    @admin.display(description='Текст')
    def short_text(self, obj):
        return obj.text[:60] + ('…' if len(obj.text) > 60 else '')
