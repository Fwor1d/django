from django import forms
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "summary", "body", "is_published")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "maxlength": 200}),
            "summary": forms.TextInput(attrs={"class": "form-control", "maxlength": 300}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "is_published": "Включите флажок, чтобы пост появился в общем списке.",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": "Ваш комментарий"}
        widgets = {"text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Напишите комментарий..."})}
