from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from Users.models import UserProfile

class SettingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'default_exposure',)
        widgets = {
            'default_exposure': forms.Select(attrs={'class': 'selectPicker form-control'})

        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


    def save(self, request):

        user = super(CreateUserForm, self).save(commit=False)
        user.is_active = True
        user.save()

        new_prof = UserProfile.objects.create(
            user=user,
        )
        new_prof.save()

        return user
