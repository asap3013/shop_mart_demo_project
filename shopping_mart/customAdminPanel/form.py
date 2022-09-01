from django import forms  
from customAdminPanel.models import *


class BannersForm(forms.ModelForm):  
    class Meta:  
        # User = get_user_model()
        model = Banners  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')