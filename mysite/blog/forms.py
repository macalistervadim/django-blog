from django import forms

import blog.models


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=True, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = blog.models.Comment
        fields = [
            blog.models.Comment.name.field.name,
            blog.models.Comment.email.field.name,
            blog.models.Comment.body.field.name,
        ]


class SearchForm(forms.Form):
    query = forms.CharField()
