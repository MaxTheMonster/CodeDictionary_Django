from django import forms
from Dictionary import models
from django.contrib.auth.forms import UserCreationForm

class CreateWordForm(forms.ModelForm):
    name = forms.CharField(label="Word", max_length=60)
    definition = forms.CharField(widget=forms.Textarea)
#    category = forms.CharField(widget=forms.HiddenInput(), required=False)
 #   hidden_css = forms.CharField(widget=forms.MostWidgets(attrs={'style': 'display:none;'}))

    class Meta:
        model = models.Word
        fields = ["name", "definition",]

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    profile_picture = forms.FileField(label = "Profile Picture", required=False)

    class Meta:
      model = models.User
      fields = ("username", "profile_picture", "email",)