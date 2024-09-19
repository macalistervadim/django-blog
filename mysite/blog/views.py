from typing import Any

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
import django.core.mail
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse
import django.shortcuts
from django.views.generic import DetailView, FormView, ListView
from taggit.models import Tag


import blog.forms
import blog.models


class PostListView(ListView):
    model = blog.models.Post
    context_object_name: str = "posts"
    paginate_by: int = 2
    template_name: str = "blog/post/list.html"

    def get_queryset(self) -> QuerySet[blog.models.Post]:
        queryset: QuerySet[blog.models.Post] = blog.models.Post.published.all()
        tag_slug: str | None = self.kwargs.get("tag_slug")
        if tag_slug:
            tag: Tag = django.shortcuts.get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        tag_slug: str | None = self.kwargs.get("tag_slug")
        if tag_slug:
            context["tag"] = django.shortcuts.get_object_or_404(
                Tag,
                slug=tag_slug,
            )
        else:
            context["tag"] = None
        return context


class PostShareView(FormView):
    form_class = blog.forms.EmailPostForm
    template_name: str = "blog/post/share.html"
    sent: bool = False  # Track email sending status

    def get_post(self) -> blog.models.Post:
        return django.shortcuts.get_object_or_404(
            klass=blog.models.Post,
            id=self.kwargs["post_id"],
            status=blog.models.Post.Status.PUBLISHED,
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["post"] = self.get_post()
        context["sent"] = self.sent
        return context

    def form_valid(self, form: blog.forms.EmailPostForm) -> HttpResponse:
        post = self.get_post()
        cd: dict[str, Any] = form.cleaned_data
        post_url: str = self.request.build_absolute_uri(
            post.get_absolute_url(),
        )
        subject: str = f"{cd['name']} recommends you read {post.title}"
        message: str = (
            f"Read {post.title} at {post_url}\n\n"
            f"{cd['name']}'s comments: {cd['comments']}"
        )
        django.core.mail.send_mail(
            subject=subject,
            message=message,
            from_email="macalistervadim@yandex.ru",
            recipient_list=[cd["to"]],
        )
        self.sent = True
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form: blog.forms.EmailPostForm) -> HttpResponse:
        self.sent = False
        return super().form_invalid(form)


class PostDetailView(DetailView):
    model = blog.models.Post
    template_name: str = "blog/post/detail.html"
    context_object_name: str = "post"

    def get_object(self) -> blog.models.Post:
        return django.shortcuts.get_object_or_404(
            blog.models.Post,
            status=blog.models.Post.Status.PUBLISHED,
            slug=self.kwargs["post"],
            publish__year=self.kwargs["year"],
            publish__month=self.kwargs["month"],
            publish__day=self.kwargs["day"],
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        post: blog.models.Post = self.get_object()
        comments: QuerySet[blog.models.Comment] = post.comments.filter(
            active=True,
        )
        form = blog.forms.CommentForm()
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts: QuerySet[blog.models.Post] = (
            blog.models.Post.published.filter(
                tags__in=post_tags_ids,
            )
            .exclude(id=post.id)
            .annotate(
                same_tags=Count("tags"),
            )
            .order_by("-same_tags", "-publish")[:4]
        )

        context["comments"] = comments
        context["form"] = form
        context["similar_posts"] = similar_posts
        return context


class PostCommentView(FormView):
    template_name: str = "blog/post/comment.html"
    form_class = blog.forms.CommentForm

    def get_post(self) -> blog.models.Post:
        return django.shortcuts.get_object_or_404(
            klass=blog.models.Post,
            id=self.kwargs["post_id"],
            status=blog.models.Post.Status.PUBLISHED,
        )

    def form_valid(self, form: blog.forms.CommentForm) -> HttpResponse:
        post: blog.models.Post = self.get_post()
        comment: blog.models.Comment = form.save(commit=False)
        comment.post = post
        comment.save()

        return self.render_to_response(
            self.get_context_data(form=form, post=post, comment=comment),
        )

    def form_invalid(self, form: blog.forms.CommentForm) -> HttpResponse:
        return self.render_to_response(
            self.get_context_data(form=form, post=self.get_post()),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["post"] = self.get_post()
        return context


class PostSearchView(FormView):
    template_name: str = "blog/post/search.html"
    form_class = blog.forms.SearchForm

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        form: blog.forms.SearchForm = self.form_class(request.GET)
        query = request.GET.get("query", None)
        results = []

        if form.is_valid() and query:
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", "body")
            search_query = SearchQuery(query)
            results = (
                blog.models.Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                )
                .filter(search=search_query)
                .order_by("-rank")
            )

        return self.render_to_response(
            self.get_context_data(form=form, results=results, query=query),
        )
