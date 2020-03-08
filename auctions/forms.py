from django import forms

from .models import Listing

from django.forms import ModelForm

from . import models
from .models import User, Listing, Comment



class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ['title', 'description', 'price', 'category', 'image_url', 'owner']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']