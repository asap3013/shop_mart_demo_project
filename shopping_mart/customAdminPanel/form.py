from django import forms  
from customAdminPanel.models import *


class BannersForm(forms.ModelForm):  
    class Meta:  
        model = Banners  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')