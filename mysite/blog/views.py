from typing import Any, Mapping, TypeAlias

import django.core.mail
from django.http import HttpRequest, HttpResponse
import django.shortcuts
from django.views.generic import FormView, ListView
from django.views.decorators.http import require_POST
from taggit.models import Tag

import blog.forms
import blog.models


class PostListView(ListView):
    model = blog.models.Post
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"

    def get_queryset(self):
        queryset = blog.models.Post.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = django.shortcuts.get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['tag'] = django.shortcuts.get_object_or_404(Tag, slug=tag_slug)
        else:
            context['tag'] = None
        return context


class PostShareView(FormView):
    form_class = blog.forms.EmailPostForm
    template_name = "blog/post/share.html"

    def get_post(self):
        return django.shortcuts.get_object_or_404(
            klass=blog.models.Post,
            id=self.kwargs["post_id"],
            status=blog.models.Post.Status.PUBLISHED,
        )

    def get_context_data(self, **kwargs) -> Mapping[str, Any]:
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_post()
        context["sent"] = getattr(self, "sent", False)
        return context

    def form_valid(self, form) -> HttpResponse:
        post = self.get_post()
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = (
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

    def form_invalid(self, form) -> HttpResponse:
        self.sent = False
        return super().form_invalid(form)


Year: TypeAlias = int
Day: TypeAlias = int
Month: TypeAlias = int


def post_detail(
    request: HttpRequest,
    year: Year,
    month: int,
    day: int,
    post: str,  # slug
) -> HttpResponse:
    post_ = django.shortcuts.get_object_or_404(
        klass=blog.models.Post,
        status=blog.models.Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post_.comments.filter(active=True)
    form = blog.forms.CommentForm()

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post_, "comments": comments, "form": form},
    )


@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = django.shortcuts.get_object_or_404(
        klass=blog.models.Post,
        id=post_id,
        status=blog.models.Post.Status.PUBLISHED,
    )
    comment = None
    form = blog.forms.CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/comment.html",
        context={"post": post,
                 "form": form,
                 "comment": comment},
    )
