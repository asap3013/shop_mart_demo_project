from django import forms
from django.core.exceptions import ValidationError
from customAdminPanel.models import *


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
            email=self.cleaned_data['email'],
            # mobile_no=self.cleaned_data['mobile_no'],
            # password1=self.cleaned_data['password1'],
            # password2=self.cleaned_data['password2']
        )  
        return user  

class Address_form(forms.ModelForm):
    # user_id = forms.CharField(label='user_id')   
    # address_1 = forms.CharField(label='address_1', min_length=5, max_length=150)
    # address_2 = forms.CharField(label='address_2', min_length=5, max_length=150)
    # city = forms.CharField(label='city', min_length=5, max_length=150)
    # country = forms.CharField(label='country')
    # state = forms.CharField(label='state')
    # zip_code = forms.IntegerField(label='zip_code')

    class Meta:
        model = UserAddress
        fields = ["user_id","address_1","address_2","city","country","state","zip_code"]

    # def address_1_clean(self):  
    #     address_1 = self.cleaned_data['address_1'].lower()  
    #     new = UserAddress.objects.filter(address_1 = address_1)  
    #     if new.count():  
    #         raise ValidationError("address_1 Already Exist")  
    #     return address_1 
    # def address_2_clean(self):  
    #     address_2 = self.cleaned_data['address_2'].lower()  
    #     new = UserAddress.objects.filter(address_2 = address_2)  
    #     if new.count():  
    #         raise ValidationError("address_2 Already Exist")  
    #     return address_2
    # def save(self, commit = True):  
    #     userAddress = UserAddress.objects.all()  
    #     return userAddress

class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email Address')
    message = forms.CharField(label='Message',min_length=5, max_length=150)


    class Meta:
        model = ContactUs
        fields = ["name","email","message"]