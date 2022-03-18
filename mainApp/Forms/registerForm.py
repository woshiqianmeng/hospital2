from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    user_name = forms.CharField(label='Your name', max_length=30)

    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.user_name = self.cleaned_data['user_name']
        if commit:
            user.save()
        return user
