# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from boat_booking.forms import BookingForm
from django.utils import timezone
from django.contrib.auth.models import User
from boat_booking.models import Booking


from schedule.models.calendars import Calendar

from schedule.models.events import Event, EventRelation
from django.http.response import JsonResponse


from django_modalview.generic.base import ModalTemplateUtilView


def custom_login(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        return login(request)
    
@login_required
def home(request):
    
    bookings = Booking.objects.all().filter(creator__pk = request.user.pk)
    
    for booking in bookings:
        print booking.event.start

    return render(request, 'home.html', {'bookings': bookings})

@login_required
def booking(request):
    if request.method == "POST":

        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.creator = request.user
            booking.submitted = timezone.now()
            
            
            data = {
                'title': booking.boat,
                'start': booking.start,
                'end': booking.end,
                'description': 'Boat booked by %s between %s and %s' % (request.user.username, booking.start, booking.end),
            }
            
            event1 = Event(**data)
            event1.save()
            
            booking.event = event1
            
            booking.save()
            
            calendar = Calendar.objects.get_or_create_calendar_for_object(User.objects.get(id=3))
            calendar.events.add(event1)
            calendar.save()
            
            EventRelation.objects.create_relation(event1, booking)
            
            return HttpResponseRedirect('../')
        else:
            print "Not valid form"
        
    else:
        
        form =  BookingForm()
    
    return render(request, 'booking/booking.html', {'form': form})


def api_occurrences(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    calendar_slug = request.GET.get('calendar_slug')

    response_data = event_occurences(start, end, calendar_slug)

    return JsonResponse(response_data, safe=False)

def event_occurences(request):
    
    response_data = []
    # Algorithm to get an id for the occurrences in fullcalendar (NOT THE SAME
    # AS IN THE DB) which are always unique.
    # Fullcalendar thinks that all their "events" with the same "event.id" in
    # their system are the same object, because it's not really built around
    # the idea of events (generators)
    # and occurrences (their events).
    # Check the "persisted" boolean value that tells it whether to change the
    # event, using the "event_id" or the occurrence with the specified "id".
    # for more info https://github.com/llazzaro/django-scheduler/pull/169

    event_list = Event.objects.all()

    for event in event_list:
        if event.event.creator.pk == request.user.pk:
            color = '#e5c442'
        else:
            color = '#93bcff'
        
        response_data.append({
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat(),
            "event_id": event.id,
            "color": color,
            "description": event.description,
            "creator": str(event.event.creator),
            "calendar": event.calendar.slug,
            })
        
    return JsonResponse(response_data, safe=False)

class BookingModal(ModalTemplateUtilView):
    
    def __init__(self, *args, **kwargs):
        super(BookingModal, self).__init__(*args, **kwargs)
            
            #self.util_button has a default value. In the components part you will see how to overide it
            #self.util_name is the name of the method that will be run. The default value is 'util', you can overide it

    def dispatch(self, request, *args, **kwargs):
        # I get an user in the db with the id parameter that is in the url.
        self.object = Booking.objects.get(pk=kwargs.get('booking_id'))
        self.title = u"Bokning av båt %s" % (self.object.boat)
        return super(BookingModal, self).dispatch(request, *args, **kwargs)
    
    def util(self, *args, **kwargs):
        '''
            url_param is the name of an url parameter. If you don't have url parameters change the signature.
        '''
        #if url_param == 'check':
        #    self.response = ModalResponse('good game', 'success') #explain in the component part
        #else:
        #    self.response = ModalResponse('Try again', 'danger')


#
#class BookingModal(ModalTemplateView):
#
#    model = Booking
#    template_name = 'modals/booking_modal.html'
#    context_object_name = 'booking_modal'
#        
#    def get(self, request, *args, **kwargs):
#        self.object = Booking.objects.filter(pk=kwargs['booking_id'])
#        return super(BookingModal, self).get(request, *args, **kwargs)
#    
#    def get_context_data(self, **kwargs):
#        context = super(BookingModal, self).get_context_data(**kwargs)
#        context['booking_id'] = self.kwargs['booking_id']
#        context['booking'] = self.object
#        return context
#    
#    def get_queryset(self):
#        return self.object.booking_set.all()
        
        
        
    