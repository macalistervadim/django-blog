from typing import TypeAlias

import django.core.mail
from django.http import HttpRequest, HttpResponse
import django.shortcuts
from django.views.generic import ListView

import blog.forms
import blog.models


class PostListView(ListView):
    queryset = blog.models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    post = django.shortcuts.get_object_or_404(
        klass=blog.models.Post,
        id=post_id,
        status=blog.models.Post.Status.PUBLISHED,
    )

    sent = False

    if request.method == "POST":
        form = blog.forms.EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd["name"]}'s comments: {cd["comments"]}"
            )
            django.core.mail.send_mail(
                subject=subject,
                message=message,
                from_email="macalistervadim@yandex.ru",
                recipient_list=[cd["to"]],
            )
            sent = True

    else:
        form = blog.forms.EmailPostForm()

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/share.html",
        context={"post": post, "form": form, "send": sent},
    )


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

    return django.shortcuts.render(
        request=request,
        template_name="blog/post/detail.html",
        context={"post": post_},
    )
