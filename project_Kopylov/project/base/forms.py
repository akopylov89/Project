from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings

# -*- coding: utf-8 -*-

class Searchbyemail(forms.Form):
    email = forms.EmailField(label='Email')

class ChangePlayerXp(forms.Form):
    xp = forms.IntegerField(label='XP')


YEAR_CHOICES = ('2016', '2017', '2018', '2019', '2020')
# MONTH_CHOICES = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

class StatPlayerGamesSearch(forms.Form):
    start_with = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=SelectDateWidget(years=YEAR_CHOICES))
    end_with = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=SelectDateWidget(years=YEAR_CHOICES))

