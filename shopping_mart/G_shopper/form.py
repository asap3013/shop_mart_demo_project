from django import forms
from django.core.exceptions import ValidationError
from customAdminPanel.models import User


class UserRegistraionForm(forms.ModelForm):  
    first_name = forms.CharField(label='First Name', min_length=5, max_length=150)  
    last_name = forms.CharField(label='Last Name', min_length=5, max_length=150) 
    username = forms.CharField(label='UserName', min_length=5, max_length=150)   
    email = forms.EmailField(label='Email Address')  
    mobile_no = forms.IntegerField(label='Mobile Number')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput) 

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "mobile_no", "password1","password2"]

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  

    def mobile_no_clean(self):
        mobile_no = self.cleaned_data['mobile_no']
        new = User.objects.filter(mobile_no=mobile_no)
        if new.count():
            raise ValidationError(" Mobile No Already Exist")  
        return mobile_no

  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['mobile_no'],
            self.cleaned_data['password1'], 
            self.cleaned_data['password2']
        )  
        return user  

