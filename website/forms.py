from flight.models import Airport
from django import forms
from django.forms import Widget
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.forms import ValidationError
from django.contrib.auth.models import User
from pprint import pprint
import datetime


DATE_FORMAT = '%d %B, %Y' # 17 April, 2015
class DatePickerWidget(Widget):
    def __init__(self, attrs=None):
        super(DatePickerWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        output = format_html(u'<input type="date" {0}>', flatatt(final_attrs))
        return output

    def value_from_datadict(self, data, files, name):
        date_data = data.get(name, '')
        try:
            D = datetime.datetime.strptime(date_data, DATE_FORMAT).date()
            return D
        except ValueError:
            return None


class FrontPageSearchForm(forms.Form):
    TRIP_TYPES = (
        ('one', 'One Way'),
        ('round', 'Round Trip')
    )
    error_css_class = 'error'
    required_css_class = 'required'

    trip_type = forms.ChoiceField(required=True,
                                  choices=TRIP_TYPES,
                                  widget=forms.RadioSelect(attrs={
                                      'class': 'with-gap'}))
    no_of_guests = forms.IntegerField(required=True)
    departure = forms.ModelChoiceField(label='From',
                                      queryset=Airport.objects.all(),
                                       required=True,
                                      empty_label=None,
                                      widget=forms.Select)
    arrival = forms.ModelChoiceField(label='To', queryset=Airport.objects.all(),
                                     required=True,
                                     widget=forms.Select)
    departure_date = forms.DateField(widget=DatePickerWidget(attrs={
        'class': 'datepicker'}), required=True, initial=datetime.date.today)
    arrival_date = forms.DateField(widget=DatePickerWidget(attrs={
        'class': 'datepicker'}), required=False)


    def clean(self):
        cleaned_data = super(FrontPageSearchForm, self).clean()
        trip_type = cleaned_data.get('trip_type', None)
        departure = cleaned_data.get('departure', None)
        arrival = cleaned_data.get('arrival', None)
        departure_date = cleaned_data.get('departure_date', None)
        arrival_date = cleaned_data.get('arrival_date', None)



        if departure and arrival:
            if departure == arrival and trip_type == 'one':
                raise ValidationError(('Invalid travel destinations'),
                                      code='invalid')

        if departure_date:
            if departure_date < datetime.date.today():
                raise ValidationError(("Choose a sensible date!"),
                                      code='invalid')

        if departure_date and arrival_date:
            if arrival_date < departure_date:
                raise forms.ValidationError(("Error! Arrival date can't be before Depature Date!"), code='invalid')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['password'].widget.attrs['placeholder'] = "Password"
        self.fields['confirm_password'].widget.attrs['placeholder'] = "Confirm Password"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password', None)
        confirm_password = cleaned_data.get('confirm_password', None)
        if password != confirm_password:
            raise ValidationError(('Passwords are not the same'), code='invalid')


class ParticularsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(ParticularsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        self.fields['password'].widget.attrs['placeholder'] = "Password"
        self.fields['confirm_password'].widget.attrs['placeholder'] = "Confirm Password"

    def clean(self):
        cleaned_data = super(ParticularsForm, self).clean()
        password = cleaned_data.get('password', None)
        confirm_password = cleaned_data.get('confirm_password', None)
        if password != confirm_password:
            raise ValidationError(('Passwords are not the same'), code='invalid')
