from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_ext = ['jpg', 'jpeg', 'png']
        ext = url.rsplit('.', 1)[1].lower()
        if ext not in valid_ext:
            raise forms.ValidationError('Unauthorized image type.')
        return url

    def save(self, force_insert=False,
             force_update=False, commit=True):
        image = super(ImageCreationForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image