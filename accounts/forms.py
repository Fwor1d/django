from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "location", "birth_date")
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }
