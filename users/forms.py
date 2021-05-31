from django.contrib.auth.forms import UserCreationForm

from .models import User


class CreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
