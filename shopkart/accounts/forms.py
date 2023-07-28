from django import forms
from .models import Account,UserProfile


class regform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password'
    }))
    class Meta:
        model = Account
        fields= ['first_name','last_name','email','password']

    def __init__(self,*args,**kwargs):
        super(regform,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last_name'

        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'

        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    def clean(self):
        cleaned_data = super(regform,self).clean()
        password =cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password does not match'
            )

class UserForm(forms.ModelForm):
    class Meta:
        model =Account
        fields = ('first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'

class UserProfileform(forms.ModelForm):
    profile_picture = forms.ImageField(required=None,error_messages = {'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileform,self).__init__(*args, **kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'