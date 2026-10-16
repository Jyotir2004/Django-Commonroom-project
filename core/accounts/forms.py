from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = super().clean_username()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email address already exists.')
        return email


class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or email',
        widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'username'}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        if username:
            identifier = username.strip()
            user = User.objects.filter(username__iexact=identifier).first()
            if user is None and '@' in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
            if user:
                self.cleaned_data['username'] = user.get_username()
        return super().clean()
