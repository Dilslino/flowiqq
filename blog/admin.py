from django.contrib import admin
from .models import Category, Tag, Post, Comment, Newsletter

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author_full_name', 'status', 'created_on', 'is_featured')
    list_filter = ('status', 'created_on', 'category', 'tags', 'is_featured')
    search_fields = ['title', 'content', 'author__username', 'author__first_name', 'author__last_name']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_on'
    ordering = ('status', '-created_on')

    def author_full_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    author_full_name.short_description = 'Author'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_on')
    search_fields = ('email',)
