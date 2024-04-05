from django import forms

from users.models import UserProfile


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("The password doesn't match!")

        del cleaned_data['password2']
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio')
