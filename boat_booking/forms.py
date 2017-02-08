from django.forms import ModelForm
from boat_booking.models import Booking
from django import forms
from django.forms.widgets import SplitDateTimeWidget
from bootstrap3_datetime.widgets import DateTimePicker

import math
import datetime
from django.utils import timezone
from schedule.models.events import Event
from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['boat', 'start', 'end']
        widgets = {
            'start': DateTimePicker(options={"format": "YYYY-MM-DD HH:00"}),
            'end': DateTimePicker(options={"format": "YYYY-MM-DD HH:00"}),
        }
    
    def clean_start(self):
        _start = self.cleaned_data['start']
        if _start < timezone.now():
            raise forms.ValidationError("The date cannot be in the past!")
        return _start
        
    def clean_end(self):
        _end = self.cleaned_data['end']
        if _end < timezone.now():
            raise forms.ValidationError("The date cannot be in the past!")
        return _end
        
    def clean(self):
        _start = self.cleaned_data['start']
        _end = self.cleaned_data['end']
        
        _end = self.cleaned_data['end']
        if _end < _start:
            raise forms.ValidationError("End date is before start date")
        
        c = _start - _end
        m = divmod(c.days * 86400 + c.seconds, 60)[0]
        if math.fabs(m) > 60 * 3:
            self.add_error('end', ValidationError('Booking longer than 3 hours'))
        
        
        _boat = self.cleaned_data['boat']
        
        bookings = Booking.objects.filter(boat__pk = _boat.pk)

        #Event.objects.filter(Q(start__day = _start.day) | Q(end__day = _end.day))
        
        for booking in bookings:
            event = booking.event
            if _start < event.end and event.start < _end:
                self.add_error('boat', ValidationError('Boat is already booked at that time.'))
        
        return self.cleaned_data
    #===========================================================================
    # def clean_start(self):
    #     start = self.cleaned_data['start']
    #     if start < timezone.now():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return start
    # 
    # def clean_end(self):
    #     start = self.cleaned_data['start']
    #     end = self.cleaned_data['end']
    #     
    #     events = Event.objects.all()
    #===========================================================================
        
        #(StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
#     def is_valid(self):
#         
#         valid = super(BookingForm, self).is_valid()
#         
#         
#         if not valid:
#             return valid
#         
#         
#         c = self.instance.start - self.instance.end
#         m = divmod(c.days * 86400 + c.seconds, 60)[0]
#         
#         if math.fabs(m) > 60 * 3:
#             self.instance.start.errors
#             return False
#             #raise forms.ValidationError("Booking longer than 3 hours")
#             #self._errors['too_long_booking'] = 'The booking was longer than 3 hours'
#             #return False
#         
#         return valid
#                 
        