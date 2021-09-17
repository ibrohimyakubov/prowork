from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, IdeaStartapper, ApplicationStaff, Startapper, Staff, CommentOfPost, COUNTRY, \
    AllUsersIdea


class RegisterForm(UserCreationForm):
    # user_types = ChoiceField(
    #                         choices=CustomUser.USER_TYPE)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'password1', 'password2', 'email', 'user_type']

        widgets = {
            'user_type': forms.Select(
                attrs={'class': "form-control"}
            )
        }


class IdeaStartapperForm(forms.ModelForm):
    class Meta:
        # file = forms.FileField()

        model = IdeaStartapper
        fields = ['title', 'description', 'file']


class AllUsersIdeaForm(forms.ModelForm):
    class Meta:
        file = forms.FileField()
        model = AllUsersIdea
        fields = ['title', 'description', 'file']


class ApplicationDeveloperForm(forms.ModelForm):
    class Meta:
        file = forms.FileField()
        model = ApplicationStaff
        fields = ['title', 'description', 'resume', 'work_type']

        widgets = {
            'work_type': forms.Select(
                attrs={'class': "form-control"}
            )
        }


class ApplicationPractitionerForm(forms.ModelForm):
    class Meta:
        file = forms.FileField()
        model = ApplicationStaff
        fields = ['title', 'description', 'resume', 'work_type']

        widgets = {
            'work_type': forms.Select(
                attrs={'class': "form-control"}
            )
        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone', 'user_type')
        widgets = {'user_type': forms.Select(attrs={'class': "form-control"})}


class StartapperUpdateForm(forms.ModelForm):
    class Meta:
        model = Startapper
        fields = ['bio', 'country', 'image']


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['bio', 'country', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentOfPost
        fields = ['comment']
