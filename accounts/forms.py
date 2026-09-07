from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        # returning errors like this means that XSS is in play
        # if a user controlled field is part of 'e'
        # then there could be some serious consequences for this code
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):

        # Ideally, forms should hide all errors related to usernames
        # this could cause username enumeration
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = ""
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
