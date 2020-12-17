from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.filter(name='User'))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username',
                  'password']
        # excludes = ['']
        
        label = {
            'password': 'Password'
        }

    def save(self):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])

        u.set_password(password)
        u.save()
        return u
