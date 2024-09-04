from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        Post.title.field.name,
        Post.slug.field.name,
        Post.author.field.name,
        Post.publish.field.name,
        Post.status.field.name,
    ]
    list_filter = [
        Post.status.field.name,
        Post.created.field.name,
        Post.publish.field.name,
        Post.author.field.name,
    ]
    search_fields = [
        Post.title.field.name,
        Post.body.field.name,
    ]
    prepopulated_fields = {Post.slug.field.name: (Post.title.field.name,)}
    raw_id_fields = [Post.author.field.name]
    date_hierarchy = Post.publish.field.name
    ordering = [
        Post.status.field.name,
        Post.publish.field.name,
    ]
