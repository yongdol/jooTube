from django import forms
from django.contrib.auth import password_validation
from member.models import MyUser


class SignupModelForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = MyUser
        fields = (
            'email',
            'password1',
            'password2',
            'last_name',
            'first_name',
            'nickname',
        )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        passoword1 = self.cleaned_data.get('password1')
        passoword2 = self.cleaned_data.get('password2')
        if passoword1 and passoword2 and passoword1 != passoword2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(
            self.cleaned_data['password2'],
            self.instance
        )
        return passoword2

    def save(self, commit=True):
        user = super(SignupModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user




class SignupForm(forms.Form):
    # https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
    # abcd = forms.ChoiceField(
    #     choices = (
    #         ('A', 'Apple'),
    #         ('B', 'Banana'),
    #     )
    # )
    email = forms.EmailField(
        max_length=100,
        error_messages={
            'invalid': '이메일 형식이 아닙니다',
        },
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nickname = forms.CharField(
        max_length=24,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
