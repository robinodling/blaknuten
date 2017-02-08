"""blaknuten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from boat_booking import views as boat_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from boat_booking.views import BookingModal
from blaknuten import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', boat_views.custom_login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^$', boat_views.home, name='home'),
    url(r'^booking/$', boat_views.booking, name='booking'),
    url(r'^fullcalendar/', TemplateView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    url(r'^api/event_occurences', boat_views.event_occurences, name='event_occurences'),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^booking_modal/(?P<booking_id>[0-9]+)', BookingModal.as_view(), name='bookingmodal')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
