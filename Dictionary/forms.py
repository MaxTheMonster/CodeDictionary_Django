from django import forms
from Dictionary import models
from django.contrib.auth.forms import UserCreationForm

class CreateWordForm(forms.ModelForm):
    name = forms.CharField(label="Word", max_length=60)
    definition = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(max_length=40)

    class Meta:
        model = models.Word
        fields = ["name", "definition", "category",]

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    profile_picture = forms.FileField(label = "Profile Picture", required=False)

    class Meta:
      model = models.User
      fields = ("username", "profile_picture", "email",)