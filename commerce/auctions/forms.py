from typing import List
from django import forms
from django.forms import fields, models, widgets

from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['description'].label = 'Description'
        self.fields['starting_bid'].label = 'Price'
        self.fields['url_image'].label = 'URL Image (optional)'
        self.fields['category'].label = 'Category (optional)'

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'starting_bid',
            'url_image',
            'category',
        ]

class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = 'Bid'

    class Meta:
        model = Bid
        fields = [
            'amount',
        ]

'''class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].label = 'Close'

    class Meta:
        model = Listing
        fields = [
            'status',
        ]'''