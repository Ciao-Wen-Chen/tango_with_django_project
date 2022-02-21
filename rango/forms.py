from django import forms 
from rango.models import Page, Category

# Chapter 7
class CategoryForm(forms.ModelForm):
    # set the field to zero by default. 
    # set the field to be hidden, user won’t be able to enter a value for these fields.
    # we will not include this hidden field at the end because they already be set the default val avoiding the "not null" error
    # for slug, we didnt include it and also set default val because our model will be responsible for populating the field when the form is eventually saved 
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information for the form
    class Meta:
        # Provide an association modelform and model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.MAX_LENGTH,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # hidding the foreign key
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data 
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://', # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data


from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    # by override this attribute, we can hide the password from user prying eyes
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)

from rango.models import UserProfile
class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
