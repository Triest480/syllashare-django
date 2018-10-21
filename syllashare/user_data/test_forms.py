from django import forms
from user_data.models import School, User


class SchoolForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Enter a School')
    city = forms.CharField(max_length=128, help_text='Enter a City')
    state = forms.CharField(max_length=128, help_text='Enter a State')

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = School


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text='Enter First Name')
    last_name = forms.CharField(max_length=128, help_text='Enter Last Name')
    email = forms.EmailField()
    class Meta:
        # Provide an association between the ModelForm and a model
        model = User

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        fields = ('first_name', 'last_name')
